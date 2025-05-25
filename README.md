## Installation

```bash
pip install https://github.com/TheArcherST/nidigr/archive/refs/heads/master.zip
```


## Usage

```bash
nidigr --help
```


```
usage: nidigr [-h] [--length LENGTH_FIXED] [--length-min LENGTH_MIN] [--length-max LENGTH_MAX] [--samples-count SAMPLES_COUNT] [--noise-factor NOISE_FACTOR] [-v]

A very simple digraph-based nickname generator. It automatically collects digraph statistics from the web (currently, statically, from some IETF standards) and generates letter sequences based on
these statistics. The first digraph is selected randomly. For the rest of the nickname, we look up digraphs that start with the last letter of the current word and choose from them. If there are
no such digraphs, we choose from all digraphs. Each choice is random but weighted according to the collected digraph statistics. Additionally, some noise is added to flatten the distribution (each
digraph's weight is increased by noise_factor * mean_weight).

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

