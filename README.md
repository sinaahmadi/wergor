# Wergor 
# Transliteration system for Kurdish


[Wergor](https://github.com/sinaahmadi/wergor) is a transliteration system for Sorani Kurdish Latin-based and Arabic-based orthographies. In this first version, we have used a rule-based method. 

### Usage
The script can be used in command-line or directly by importing the `Wergor class` in your codes.

#### Command-line usage

~~~
python Wergor.py -<mode> <input file>.txt
~~~
Currently `-arabic2latin` and `-latin2arabic` are the only defined modes. The input file should be in `.txt` format. By running the script, the output file is automatically created in the same directory with "_transliterated" added to the name of the input file.

#### Importing *Wergor* class in the *Wergor* module

 
~~~python
import Wergor
# Arabic to Latin transliteration
wergor_transliterator = Wergor.Wergor("-arabic2latin")
print wergor_transliterator._transliterate(u"هەڵاوێر")

# Latin to Arabic transliteration
wergor_transliterator = Wergor.Wergor("-latin2arabic")
print wergor_transliterator._transliterate(u"birayetî")

# Syllable detection based on the defined patterns (not complete)
wergor_transliterator = Wergor.Wergor("-latin2arabic")
print wergor_transliterator._syllable_detector(u"henase")
~~~

This script yields the folowing outputs: 

~~~
heławêr
برایەتی
[('CV', 'CV', 'CV'), ('CV', 'CVC', 'V'), ('CVC', 'V', 'CV'), ('CVC', 'VC', 'V')]
~~~

Presently the Wergor transliterator only supports UTF-8 encoding. If not interested in getting red lines in your console make sure to encode your strings in UTF-8 or simply add `u` to the beginning of your strings (i.e., `word1 = u"جوان"`). 

For each orthography, two text files are provided in the *examples* folder that you can test. Note that `_syllable_detector()` which suggests the possible syllable structures in a given word is not an option for the command-line usage. 

### Wergor corpus

If you are interested in the task of transliteration or you are going to study the existing challenges in the Sorani Kurdish text processing more in depth, Wergor corpus can help you. Wergor corpus includes 20k manually transliterated Sorani Kurdish words in the Arabic-based and the Latin-based orthographies. 

If you're using a character-level model, you may use `transliteration_data_set.pickle` in the `dataset` folder. This file contains the preprocessed tokens in the corpus. By unpickling this file, you have a list of tuples containing a token with its transliteration. Our tokenization is based on the space delimiter.


### Requirements
  * KurdITGroup keyboard ([Download](https://www.kurditgroup.org/downloads)).
  * Python 2.7


### Reference
If you're using Wergor transliterator in your researches, please don't forget to cite our paper. 

~~~
 Sina Ahmadi. A Rule-based Kurdish Text Transliteration System. 
~~~

This helps us to also find your work easily.

### License

This project is available under [MIT Licence](https://opensource.org/licenses/mit-license.php).