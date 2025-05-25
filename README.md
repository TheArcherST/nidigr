## Installation

```bash
pip install https://github.com/TheArcherST/nidigr
```


## Usage

```bash
nidigr --help
```


```
usage: nidigr [-h] [--length LENGTH_FIXED] [--length-min LENGTH_MIN] [--length-max LENGTH_MAX] [--samples-count SAMPLES_COUNT] [--noise-factor NOISE_FACTOR] [-v]

Very simple digraph-based nickname generator. Automatically collects digraph statitics from web (currently, statically, from some IETF standards), and generates letter sequences based on this
statistics. First digraph is selects randomly, than, for the rest of nickname, wee lookup for digraphs that starts from last letter of word, and choise from them. If there are no such digraphs, we
choise from all digraphs. Each choise is random but weighted with collected digraphs statistics. Also there is a noise added that is flattenizes distribution (each digraph weight is increased by
`noise_factor * mean_weight`).

options:
  -h, --help            show this help message and exit
  --length LENGTH_FIXED
  --length-min LENGTH_MIN
  --length-max LENGTH_MAX
  --samples-count SAMPLES_COUNT
  --noise-factor NOISE_FACTOR
                        It seems that you can think about it as about LLM models temperature.
  -v                    Verbose output

```
