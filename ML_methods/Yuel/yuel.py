import os, sys, io, time, argparse, re, random, datetime

def get_parser():
  parser = argparse.ArgumentParser()

  parser.add_argument('type', type=str, help='train|predict')
  
  parser.add_argument('--data', '-d', type=str, default='data/pdbbind-train.tsv', help='training set')
  parser.add_argument('--out', '-o', type=str, default='out.txt', help='output')
  parser.add_argument('--batch_size', '-b', type=int, default=100, help='batch size')
  parser.add_argument('--comp_size', '-c', type=int, default=64, help='max number of atoms in a compound')
  parser.add_argument('--prot_size', '-p', type=int, default=1024, help='max number of residues in a protein')
  parser.add_argument('--blosum62', '-s', type=str, default='data/blosum62.txt', help='path of blosum62 file')
  parser.add_argument('--nfeat', '-e', type=int, default=32, help='number of features')
  parser.add_argument('--num_conv_layers', type=int, default=3, help='num of convolution layers')
  parser.add_argument('--num_graph_layers', type=int, default=3, help='num of graph layers')
  parser.add_argument('--num_attention_layers', type=int, default=2, help='num of attention layers')
  parser.add_argument('--epochs', type=int, default=50, help='num of epochs')
  parser.add_argument('--model', type=str, default='models/davis.model', help='model')
  parser.add_argument('--cpt_path', type=str, default='checkpoints', help='checkpoint path')
  parser.add_argument('--cpt_name', type=str, default='model', help='checkpoint name')
  parser.add_argument('--compound_column', type=str, default='Compound', help='compound column in the dataset file')
  parser.add_argument('--compound_type_column', type=str, default='CompType', help='type of the compound')
  parser.add_argument('--protein_column', type=str, default='Protein', help='protein column in the dataset file')
  parser.add_argument('--affinity_column', type=str, default='Affinity', help='affinity column in the dataset file')
  parser.add_argument('--learning_rate', type=float, default=0.001, help='learning rate')
  parser.add_argument('--gpu', type=int, default=-1, help='GPU')

  return parser

if __name__ == '__main__':
  parser = get_parser()
  args = parser.parse_args()
  os.environ["CUDA_VISIBLE_DEVICES"]='{0}'.format(args.gpu)
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import RDConfig
from rdkit.Chem import FragmentCatalog
from rdkit.Chem import DataStructs
import tensorflow_probability as tfp
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sonnet as snt
import graph_nets as gn
from graph_nets import utils_np
from graph_nets import utils_tf
from graph_nets import graphs
from rdkit import RDLogger
import scipy.stats
RDLogger.DisableLog('rdApp.*')

def new_proc(opt):
  proc = type('Proc', (object,), {})() # create an empty object to contain global variables
  for arg in vars(opt):
    val = getattr(opt, arg)
    setattr(proc, arg, val)
  return proc

def print_gpu(igpu=0):
  gpus = tf.config.list_physical_devices('GPU')
  logical_gpus = tf.config.experimental.list_logical_devices('GPU')
  print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")

def array2string(arr):
  buf = io.StringIO()
  n = len(arr.shape)
  if np.isscalar(arr):
    buf.write(str(arr))
  else:
    buf.write('[')
    buf.write(','.join(array2string(i) for i in arr))
    buf.write(']')

  return buf.getvalue()

def get_mol_dict():
    if os.path.exists('data/mol_dict'):
        with open('data/mol_dict', 'rb') as f:
            mol_dict = pickle.load(f)
#             mol_dict = pickle.load(f, encoding='latin1')
    else:
        names = []
        mol_dict = {}
        mols = Chem.SDMolSupplier('data/Components-pub.sdf')
#         mols = Chem.SDMolSupplier('data/Components-pub.sdf',removeHs=False)
        for m in mols:
            if m is None:
                continue
            name = m.GetProp("_Name")
            names.append(name)
            mol_dict[name] = m
        with open('data/mol-names.txt', 'w+') as f:
            for name in names:
              f.write('{0}\n'.format(name))
        with open('data/mol_dict', 'wb') as f:
            pickle.dump(mol_dict, f)
    return mol_dict

# Compound Feature
class CompFeat():
  def __init__(self, proc):
    self.elem_list = ['C', 'N', 'O', 'S', 'F', 'Si', 'P', 'Cl', 'Br', 'Mg', 'Na', 'Ca', 'Fe', 'As', 'Al', 'I', 'B', 'V', 'K', 'Tl', 'Yb', 'Sb', 'Sn', 'Ag', 'Pd', 'Co', 'Se', 'Ti', 'Zn', 'H', 'Li', 'Ge', 'Cu', 'Au', 'Ni', 'Cd', 'In', 'Mn', 'Zr', 'Cr', 'Pt', 'Hg', 'Pb', 'W', 'Ru', 'Nb', 'Re', 'Te', 'Rh', 'Tc', 'Ba', 'Bi', 'Hf', 'Mo', 'U', 'Sm', 'Os', 'Ir', 'Ce','Gd','Ga','Cs', 'unknown']
    self.n_atomfeatures = len(self.elem_list) + 6 + 6 + 6 + 1
    self.n_bondfeatures = 6

    self.comp_size = proc.comp_size

  def onehot(self, x, allowable_set):
    return [x == s for s in allowable_set]

  def atom_features(self, atom):
    return np.array(self.onehot(atom.GetSymbol(), self.elem_list) 
                    + self.onehot(atom.GetDegree(), [0,1,2,3,4,5]) 
                    + self.onehot(atom.GetExplicitValence(), [1,2,3,4,5,6])
                    + self.onehot(atom.GetImplicitValence(), [0,1,2,3,4,5])
                    + [atom.GetIsAromatic()], dtype=np.float32)

  def bond_features(self, bond):
    bt = bond.GetBondType()
    return np.array([bt == Chem.rdchem.BondType.SINGLE, bt == Chem.rdchem.BondType.DOUBLE, bt == Chem.rdchem.BondType.TRIPLE, \
                     bt == Chem.rdchem.BondType.AROMATIC, bond.GetIsConjugated(), bond.IsInRing()], dtype=np.float32)

  def __call__(self, mol):
    n_atoms = mol.GetNumAtoms()
    n_bonds = mol.GetNumBonds()
    assert n_atoms <= self.comp_size
    assert n_bonds >= 0

    nodes = np.zeros((self.comp_size,self.n_atomfeatures), dtype=np.float32)
    edges = np.zeros((n_bonds,self.n_bondfeatures), dtype=np.float32)
    senders = np.zeros((n_bonds,), dtype=np.int32)
    receivers = np.zeros((n_bonds,), dtype=np.int32)

    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        nodes[idx] = self.atom_features(atom)

    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtom().GetIdx()
        a2 = bond.GetEndAtom().GetIdx()
        idx = bond.GetIdx()
        edges[idx] = self.bond_features(bond)
        senders[idx] = a1
        receivers[idx] = a2

    data_dict = {
      "globals": [],
      "nodes": nodes,
      "edges": edges,
      "senders": senders,
      "receivers": receivers
    }
    data_dicts = [data_dict]
    graphs_tuple_tf = utils_tf.data_dicts_to_graphs_tuple(data_dicts)

    return graphs_tuple_tf

# Protein Feature
class ProtFeat():
  def __init__(self, proc):
    self.prot_size = proc.prot_size
    self.blosum62 = proc.blosum62

    self.aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    self.blosum_dict = dict()
    iline = 0
    for line in open(self.blosum62):
      if iline > 0:
        l = re.split('\s+', line.strip())
        self.blosum_dict[l[0]] = np.array(l[1:]).astype(float)
      iline += 1

  def __call__(self, seq):
    n = len(seq)
    assert n <= self.prot_size
    arr = np.zeros((self.prot_size, 20))
    for i, c in enumerate(seq):
      if c in self.blosum_dict:
        arr[i] = self.blosum_dict[c]
    return arr

class DataLoader():
  def __init__(self, proc):
    self.batch_size = proc.batch_size
    self.data_file = proc.data
    self.comp_size = proc.comp_size
    self.prot_size = proc.prot_size
    self.comp_feat = CompFeat(proc)
    self.prot_feat = ProtFeat(proc)

    self.df = pd.read_csv(self.data_file)
    self.comp_list = self.df[proc.compound_column].values
    self.prot_list = self.df[proc.protein_column].values
    self.aff_list = self.df[proc.affinity_column].values
    self.comp_type_list = self.df[proc.compound_type_column].values
    
    self.index = 0
    self.rows = len(self.aff_list)
    self.indices = list(range(self.rows))
    
    self.mol_dict = get_mol_dict()

  def init(self):
    self.index = 0
    return self
    
  def shuffle(self):
    random.shuffle(self.indices)
    return self
    
  def load(self):
    prot, comp, nprot, ncomp, aff, ind = [], [], [], [], [], []
    i = 0
    while (True):
      if i == self.batch_size:
        prot = tf.convert_to_tensor(prot, tf.float32)
        nprot = tf.convert_to_tensor(nprot, tf.float32)
        comp = utils_tf.concat(comp, axis=0)
        ncomp = tf.convert_to_tensor(ncomp, tf.float32)
        aff = tf.convert_to_tensor(aff, tf.float32)
        return prot, comp, aff, nprot, ncomp, ind

      if self.index >= self.rows:
        return None
      
      index = self.indices[self.index]
      compstr, sequence, affinity, comp_type = self.comp_list[index], self.prot_list[index], self.aff_list[index], self.comp_type_list[index]
      mol = None
      if comp_type == 'smi':
        mol = Chem.MolFromSmiles(compstr)
#         if mol:
#           mol = Chem.AddHs(mol)
      elif comp_type == 'inchi':
        mol = Chem.MolFromInchi(compstr)
#         if mol:
#           mol = Chem.AddHs(mol)
      elif comp_type == 'sdf':
        if compstr in self.mol_dict:
          mol = self.mol_dict[compstr]
#       print(mol.GetNumAtoms(), len(sequence), affinity)
      if mol and mol.GetNumAtoms() <= self.comp_size and len(sequence) <= self.prot_size:
        prot.append(self.prot_feat(sequence))
        nprot.append(len(sequence))
        comp.append(self.comp_feat(mol))
        ncomp.append(mol.GetNumAtoms())
#         aff.append(np.log10(affinity))
        aff.append(affinity)
        ind.append(index)
        i += 1
      self.index += 1

class Attention(snt.Module):
  def __init__(self, nfeat):
    super(Attention, self).__init__()

    self.nfeat = nfeat
    self.nlinears = 5
    self.nattfeat = nfeat*50

    self.prot_linear1 = snt.Linear(output_size=self.nattfeat, with_bias=False)
    self.comp_linear1 = snt.Linear(output_size=self.nattfeat, with_bias=False)
    
    self.prot_linears = [snt.Linear(output_size=nfeat*8) for i in range(self.nlinears)]
    self.comp_linears = [snt.Linear(output_size=nfeat*8) for i in range(self.nlinears)]
    
  def __call__(self, x_comp, x_prot, mask_comp, mask_prot):
    for i in range(self.nlinears):
      x_comp = self.comp_linears[i](x_comp)
      x_comp = tf.nn.leaky_relu(x_comp)
      x_prot = self.prot_linears[i](x_prot)
      x_prot = tf.nn.leaky_relu(x_prot)
    
    x_comp = self.comp_linear1(x_comp) # batch comp nfeat*20
    x_prot = self.prot_linear1(x_prot) # batch prot nfeat*20
    mask_comp1 = tf.tile(mask_comp[:,:,tf.newaxis], tf.constant([1,1,self.nattfeat], tf.int32))
    mask_prot1 = tf.tile(mask_prot[:,:,tf.newaxis], tf.constant([1,1,self.nattfeat], tf.int32))
    att = tf.matmul(x_comp*mask_comp1, x_prot*mask_prot1, transpose_b=True) # batch comp prot

    return att

class Yuel(snt.Module):
  def __init__(self, proc):
    super(Yuel, self).__init__()

    self.num_attention_layers = proc.num_attention_layers
    self.num_graph_layers = proc.num_graph_layers
    self.num_conv_layers = proc.num_conv_layers
    self.nfeat = proc.nfeat
    self.batch_size = proc.batch_size
    self.prot_size = proc.prot_size
    self.comp_size = proc.comp_size
    
    self.comp_graph1 = gn.modules.GraphNetwork(
      edge_model_fn=lambda: snt.Linear(output_size=self.nfeat),
      node_model_fn=lambda: snt.Linear(output_size=self.nfeat),
      global_model_fn=lambda: snt.Linear(output_size=1))
    
    self.comp_graph2 = gn.modules.GraphNetwork(
      edge_model_fn=lambda: snt.Linear(output_size=self.nfeat),
      node_model_fn=lambda: snt.Linear(output_size=self.nfeat),
      global_model_fn=lambda: snt.Linear(output_size=1))
    
    self.convs = [snt.Conv1D(output_channels=self.nfeat, kernel_shape=3) for i in range(3)]
    self.dropout = snt.Dropout(rate=0.05)

    self.prot_linear = snt.Linear(output_size=self.nfeat)
  
    self.attention = Attention(self.nfeat)
  
  def __call__(self, x_comp, x_prot, mask_comp, mask_prot, is_training):
    x_comp1 = self.comp_graph1(x_comp)
    x_comp2 = self.comp_graph2(x_comp1)
    x_comp3 = tf.reshape(x_comp2.nodes, (-1, self.comp_size, self.nfeat)) # batch comp nfeat

    x_prot1 = self.prot_linear(x_prot)
    x_prot2 = self.convs[0](x_prot1)
    x_prot3 = self.convs[1](x_prot2)
    x_prot4 = self.convs[2](x_prot3)
    x_prot5 = tf.concat([x_prot1, x_prot2, x_prot3, x_prot4], axis=-1) # batch prot nfeat

    aff_int = self.attention(x_comp3, x_prot5, mask_comp, mask_prot) # batch comp prot
    aff_int = self.dropout(aff_int, is_training=is_training)
    aff_comp = tf.reduce_max(aff_int, axis=-1) # batch comp
    aff = tf.reduce_sum(aff_comp, axis=-1) # batch

    return aff, aff_int

def loss_function(aff, aff_inter, real):
  return tf.square(aff-real)

def accuracy_function(prediction, y):
  unexplained_error = tf.reduce_sum(tf.square(y-prediction))
  total_error = tf.reduce_sum(tf.square(y-tf.reduce_mean(y)))
  R_squared = 1-tf.divide(unexplained_error, total_error)
  return R_squared

def create_mask(shape, ls):
  arr = np.ones(shape)
  for i, n in enumerate(ls.numpy()):
    arr[i, int(n):] = 0
  return tf.convert_to_tensor(arr, tf.float32)

def set_checkpoint(proc, model):
  checkpoint_root = proc.cpt_path
  checkpoint_name = proc.cpt_name
  save_prefix = os.path.join(checkpoint_root, checkpoint_name)
  checkpoint = tf.train.Checkpoint(module=model)
  latest = tf.train.latest_checkpoint(checkpoint_root)
  if latest is not None:
    checkpoint.restore(latest)
  return checkpoint, save_prefix

def num_parameters(model):
  return np.sum([np.prod(v.get_shape().as_list()) for v in model.trainable_variables])

def save_model(my_module, proc):
  input_signature = [
    graphs.GraphsTuple(nodes=tf.TensorSpec(shape=(None, 82), dtype=tf.float32, name=None),
                edges=tf.TensorSpec(shape=(None, 6), dtype=tf.float32, name=None),
                receivers=tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None),
                senders=tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None),
                globals=tf.TensorSpec(shape=(None, 0), dtype=tf.float32, name=None),
                n_node=tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None),
                n_edge=tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None)),
    tf.TensorSpec([None, proc.prot_size, 20]),
    tf.TensorSpec([None, proc.comp_size]),
    tf.TensorSpec([None, proc.prot_size]),
    tf.TensorSpec(shape=None, dtype=tf.bool)
  ]
  
  @tf.function(input_signature=input_signature)
  def inference(comp, prot, mask_comp, mask_prot, is_training):
    return my_module(comp, prot, mask_comp, mask_prot, is_training)

  to_save = snt.Module()
  to_save.inference = inference
  to_save.all_variables = list(my_module.variables)
  tf.saved_model.save(to_save, proc.model)

def train(proc):
  start_time = time.time()
  yuel = Yuel(proc)
  loader = DataLoader(proc)
  checkpoint, save_prefix = set_checkpoint(proc, yuel)
  
  opt = snt.optimizers.Adam(learning_rate=proc.learning_rate)
  
  def training_step(comp, prot, mask_comp, mask_prot, affinity):
    with tf.GradientTape() as tape:
      aff, aff_inter = yuel(comp, prot, mask_comp, mask_prot, True)
      loss = loss_function(aff, aff_inter, affinity)

    params = yuel.trainable_variables
    grads = tape.gradient(loss, params)
    opt.apply(grads, params)
    return loss, aff, aff_inter
  
  prot, comp, affinity, nprot, ncomp, ind = loader.load()
  input_signature = [
    utils_tf.specs_from_graphs_tuple(comp),
    tf.TensorSpec.from_tensor(prot),
    tf.TensorSpec([proc.batch_size, proc.comp_size]),
    tf.TensorSpec([proc.batch_size, proc.prot_size]),
    tf.TensorSpec.from_tensor(affinity)
  ]
  training_step = tf.function(training_step, input_signature=input_signature)

  logdir = "logs/train/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  summary_writer = tf.summary.create_file_writer(logdir=logdir)

  step = 0
  affs1 = []
  affs2 = []
  for epoch in range(proc.epochs):
    loader.shuffle().init()
    while True:
      data = loader.load()
      if data is None:
        break
      prot, comp, affinity, nprot, ncomp, ind = data
      mask_comp = create_mask([proc.batch_size, proc.comp_size], ncomp)
      mask_prot = create_mask([proc.batch_size, proc.prot_size], nprot)
      loss, aff, aff_inter = training_step(comp, prot, mask_comp, mask_prot, affinity)
  
      for i in range(proc.batch_size):
        affs1.append(affinity.numpy()[i])
        affs2.append(aff.numpy()[i])

      if step == 0:
        print('Number of parameters: {0}'.format(num_parameters(yuel)))

      if step % 10 == 9:
        with summary_writer.as_default():
          tf.summary.scalar('loss', np.mean(loss.numpy()), step=step)
          slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(affs1, affs2)
          accuracy = r_value
          tf.summary.scalar('accuracy', accuracy, step=step)
          print('Epoch {0:08d}, Step {1:08d}, Loss: {2:15.3f}, Accuracy: {3:8.3f}, Time: {4:8.3f} min'.format(epoch, step, np.mean(loss.numpy()), accuracy, (time.time()-start_time)/60.0), end='\r')
          affs1, affs2 = [], []

      if step % 1000 == 0:
        checkpoint.save(save_prefix)

      step += 1
    print('')
  checkpoint.save(save_prefix)
  save_model(yuel, proc)

def predict(proc):
  loader = DataLoader(proc)
  yuel = tf.saved_model.load(proc.model)
  
  total, correct = 0.0, 0.0
  inds, affs, aff_prots, aff_comps, aff_indices = [], [], [], [], []
  while True:
    data = loader.load()
    if data is None:
      break
    prot, comp, affinity, nprot, ncomp, ind = data
    batch_size = prot.shape[0]
    print('{0:08d}/{1:08d}'.format(ind[-1]+1, loader.rows), end='\r', flush=True)
    inds += ind
    mask_comp = create_mask([batch_size, proc.comp_size], ncomp)
    mask_prot = create_mask([batch_size, proc.prot_size], nprot)
    affinity_, attention = yuel.inference(comp, prot, mask_comp, mask_prot, False)
    aff_prot = tf.reduce_sum(attention, axis=1).numpy()
    aff_comp = tf.reduce_sum(attention, axis=2).numpy()
    count = accuracy_function(affinity_, affinity)
    correct += count.numpy()
    total += batch_size
    nprot = nprot.numpy()
    ncomp = ncomp.numpy()
    for i in range(batch_size):
      affs.append(affinity_.numpy()[i])
      aff_prots.append(aff_prot[i,:int(nprot[i])])
      aff_comps.append(aff_comp[i,:int(ncomp[i])])

  j = 0
  affs2, aff_prots2, aff_comps2, aff_indices2 = [], [], [], []
  for i in range(loader.rows):
    if i in inds:
      affs2.append(affs[j])
      aff_prots2.append(array2string(aff_prots[j]))
      aff_comps2.append(array2string(aff_comps[j]))
      j += 1
    else:
      affs2.append(np.nan)
      aff_prots2.append(np.nan)
      aff_comps2.append(np.nan)

#  df = pd.DataFrame(data={'Affinity':affs2,'ProtAff':aff_prots2,'CompAff':aff_comps2})
  df = pd.DataFrame(data={'Affinity':affs2})
  df.to_csv(proc.out)
  
  print('Done                    ')

if __name__ == '__main__':
  proc = new_proc(args)
  if proc.type == 'train':
    train(proc)
  elif proc.type == 'predict':
    predict(proc)


