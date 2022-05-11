This is the repository for the TensorFuzz tool with further additions. To see the original project go here: https://github.com/brain-research/tensorfuzz

The additions and distribution of this project is purely for research reasons, which is allowed by the original work authors under their License.

The current additions include three neural networks related to: mnist, cifar10, cats vs dogs datasets.
## Installation

You ought to be able to run the code in this repository by doing the following:
```
git checkout master
```


```
conda create --name smth python=3.6
conda activate smth
```



```
pip install -r requirements.txt
```

Then do:

```
export PYTHONPATH="$PYTHONPATH:$HOME/tensorfuzz"
```
## Examples
To run my Simple DNN to search for numerical erros use functions:
```
python examples/nans/nan_simple_model.py --checkpoint_dir=/tmp/nanfuzzer --data_dir=/tmp/mnist --training_steps=35000 --init_scale=0.25
```
```
python examples/nans/nan_fuzzer.py --checkpoint_dir=/tmp/nanfuzzer --total_inputs_to_fuzz=1000000 --mutations_per_corpus_item=100 --alsologtostderr --ann_threshold=0.5
```


To run quantization and disagreement finding run:
```
python examples/quantize/quantized_simple_model.py --checkpoint_dir='/tmp/quantized_checkpoints_2' --training_steps=10000
```

```
python examples/quantize/quantized_fuzzer.py --checkpoint_dir=/tmp/quantized_checkpoints_2 --total_inputs_to_fuzz=1000000 --mutations_per_corpus_item=100 --alsologtostderr --output_path=/tmp/quantized_image.png --ann_threshold=1.0 --perturbation_constraint=1.0 --strategy=ann
```
