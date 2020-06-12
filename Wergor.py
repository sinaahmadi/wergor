# -*- coding: utf-8 -*-
"""
Created on Tue May  9 00:45:08 2017
 @author: Sina Ahmadi
"""
import os
import codecs
import sys
import itertools
reload(sys)  
sys.setdefaultencoding('utf-8') 
#==============================================================================
#  Please note that only "UTF-8" encoding is accepted by the transliteration system.
#==============================================================================
class Wergor:
    def __init__(self, mode):		
        self.mode = mode
        self.UNKNOWN = u"�"
        self.characters_mapping = {u"a" : u"ا",
                                    u"b" : u"ب",
                                    u"c" : u"ج",
                                    u"ç" : u"چ",
                                    u"d" : u"د",
                                    u"e" : u"ە",
                                    u"ê" : u"ێ",
                                    u"f" : u"ف",
                                    u"g" : u"گ",
                                    u"h" : u"ه",
                                    u"ḧ" : u"ح",
                                    u"j" : u"ژ",
                                    u"k" : u"ک",
                                    u"l" : u"ل",
                                    u"ł" : u"ڵ",
                                    u"m" : u"م",
                                    u"n" : u"ن",
                                    u"o" : u"ۆ",
                                    u"p" : u"پ",
                                    u"q" : u"ق",
                                    u"r" : u"ر",
                                    u"ř" : u"ڕ",
                                    u"s" : u"س",
                                    u"ş" : u"ش",
                                    u"t" : u"ت",
                                    u"û" : u"وو",
                                    u"û" : u"û",
                                    u"v" : u"ڤ",
                                    u"x" : u"خ",
                                    u"z" : u"ز",
                                    u"ẍ" : u"غ",
                                    u"u" : u"u",
                                    u"w" : u"w",
                                    u"y" : u"y",
                                    u"î" : u"î",
                                    u"i" : u"i",
                                    u"ë" : u"ع"}
        self.digits_mapping= {u"۰" : u"0", 
                                    u"۱" : u"1",
                                    u"۲" : u"2",
                                    u"۳" : u"3",
                                    u"۴" : u"4",
                                    u"۵" : u"5",
                                    u"۶" : u"6",
                                    u"۷" : u"7",
                                    u"۸" : u"8",
                                    u"۹" : u"9",
                                    u"٠" : u"0",
                                    u"١" : u"1",
                                    u"٢" : u"2",
                                    u"٣" : u"3",
                                    u"٤" : u"4",
                                    u"٥" : u"5",
                                    u"٦" : u"6",
                                    u"٧" : u"7",
                                    u"٨" : u"8",
                                    u"9" : u"٩"}
        self.punctuation_mapping = {u"!" : u"!",
                                    u"\\" : u"\\",
                                    u"#" : u"#",
                                    u"$" : u"$",
                                    u"%" : u"%",
                                    u"&" : u"&",
                                    u"'" : u"'",
                                    u"(" : u"(",
                                    u")" : u")",
                                    u"*" : u"*",
                                    u"+" : u"+",
                                    u"÷" : u"÷",
                                    u"=" : u"=",
                                    u"," : u"،",
                                    u"-" : u"-",
                                    u"." : u".",
                                    u"/" : u"/",
                                    u":" : u":",
                                    u";" : u"؛",
                                    u"<" : u"<",
                                    u">" : u">",
                                    u"?" : u"؟",
                                    u"@" : u"@",
                                    u"^" : u"^",
                                    u"_" : u"_",
                                    u"`" : u"`",
                                    u"{" : u"{",
                                    u"}" : u"}",
                                    u"|" : u"|",
                                    u"]" : u"]",
                                    u"[" : u"[",
                                    u"~" : u"~",
                                    u"\"" : u"\""}
        self.tricky_characters = {u"ك" : u"ک",
                                  u"آ" : u"ا",
                                  u"ة" : u"ە",
                                  u"إ" : u"ا",
                                  u"ي" : u"ی",
                                  u"أ" : u"ا"}
        self.wy_mappings = {u"u":u"و",u"w":u"و",u"y":u"ی",u"î":u"ی"}

        self.hemze = u"ئ"
        self.bizroke = u"i"
        self.uw_iy_forms = {"target_char_vowel":[u"î",u"u"], "target_char_cons":[u"y",u"w"]}
        self.target_char = [u"و", u"ی"]
        self.arabic_vowels = list(u"اîiەûێoۆ")
        self.arabic_cons = list(u"بپتشسرڕژڤڵقفغعهخحجچلنمکگزدwy")
        
        self.latin_vowels = list(u"aîeûêuoi")
        self.latin_cons = list(u"bptşsrřjvłqfẍëhxḧcçlnmkgzdwy")
        
        self.characters_pack = {"-arabic2latin":self.characters_mapping.values(), "-latin2arabic":self.characters_mapping.keys()}
#==============================================================================
#   Main methhod of the class 
#==============================================================================
    def _transliterate(self, word):
        if(self.mode == "-arabic2latin"):
            # w/y detection based on the priority in "word"
            for char in word:
                if(char in self.target_char):
                    word = self._uw_iy_Detector(word, char)  
            if(word[0]==self.hemze and word[1] in self.arabic_vowels):
                word = word[1:]
            word = list(word)
            for char_index in range(len(word)):
                word[char_index] = self._arabic2latin(word[char_index])
            word = "".join(word)
            word = self._bizrokeFinder(word)
        elif(self.mode == "-latin2arabic"):
            word = list( word.replace(self.bizroke, "") )
            if(len(word) > 0):
                for char_index in range(len(word)):
                    word[char_index] = self._latin2arabic(word[char_index])
                if(word[0] in self.arabic_vowels):
                    word.insert(0, self.hemze)
                word = "".join(word).replace(u"û", u"وو")
            else:
                return self.UNKNOWN
        return word
#==============================================================================
#   Preprocessing by normalizing text encoding and removing embedding characters
#==============================================================================
    def _preprocessor(self, word):
        word = list(word.replace(u'\u202b', "").replace(u'\u202c', "").replace(u'\u202a', "").replace(u"وو", u"û").replace(u"\u200c", "").replace(u"ـ", ""))
        for char_index in range(len(word)):
            if(word[char_index] in self.tricky_characters.keys()):
                word[char_index] = self.tricky_characters[word[char_index]]
        return "".join(word)
#==============================================================================
#   Detection of "و" and "ی" in the Arabic-based orthography
#==============================================================================
    def _uw_iy_Detector(self, word, target_char):
        word = list(word)
        if(target_char == u"و"):
            dic_index = 1
        else:
            dic_index = 0
        
        if(word == target_char):
            word = self.uw_iy_forms["target_char_cons"][dic_index]
        else:
            for index in range(len(word)):
                if(word[index] == self.hemze and word[index+1] == target_char):
                    word[index+1] = self.uw_iy_forms["target_char_vowel"][dic_index]
                    index += 1
                else:
                    if(word[index] == target_char):
                        if(index==0):
                            word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                        else:
                            if(word[index-1] in self.arabic_vowels):
                                word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                            else:
                                if(index+1 <len(word)):
                                    if(word[index+1] in self.arabic_vowels):
                                        word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                                    else:
                                        word[index] = self.uw_iy_forms["target_char_vowel"][dic_index]
                                else:
                                    word[index] = self.uw_iy_forms["target_char_vowel"][dic_index]

        word = "".join(word).replace(self.hemze+self.uw_iy_forms["target_char_vowel"][dic_index], self.uw_iy_forms["target_char_vowel"][dic_index])
        return word
#==============================================================================
#   Detection of the syllable based on the given pattern. May be used for transcription applicaitons.
#==============================================================================
    def _syllable_detector(self, word):
        syllable_templates = ["V", "VC", "VCC", "CV", "CVC", "CVCCC"]
        CV_converted_list = ""       
        for char in word:
            if(char in self.latin_vowels):
                CV_converted_list += "V"
            else:
                CV_converted_list += "C"
        
        syllables = list()
        for i in range(1,len(CV_converted_list)):
            syllable_templates_permutated = [p for p in itertools.product(syllable_templates, repeat=i)]
            for syl in syllable_templates_permutated:
                if(len("".join(syl))==len(CV_converted_list)):
                    if(CV_converted_list == "".join(syl) and "VV" not in "".join(syl)):
                        syllables.append(syl)
        return syllables
#==============================================================================
#   Detection of the "i" character in the Arabic-based orthography. Incomplete version.
#==============================================================================
    def _bizrokeFinder(self, word):
        word = list(word)
        if(len(word) >2 and word[0] in self.latin_cons and word[1] in self.latin_cons and word[1] != u"w" and word[1] != u"y"):
            word.insert(1, u"i")
        return "".join(word)
#==============================================================================
#   Mapping Arabic-based characters to the Latin-based equivalents
#==============================================================================
    def _arabic2latin(self, char):
        if(char != ""):
            if(char in self.characters_mapping.values()):
                return self.characters_mapping.keys()[self.characters_mapping.values().index(char)]
            if(char in self.punctuation_mapping.values()):
                return self.punctuation_mapping.keys()[self.punctuation_mapping.values().index(char)]
            if(char in self.digits_mapping.values()):
                return self.digits_mapping.keys()[self.digits_mapping.values().index(char)]
            if(char in self.punctuation_mapping):
                return self.punctuation_mapping[char]
            if(char in self.digits_mapping):
                return self.digits_mapping[char]
        return self.UNKNOWN
#==============================================================================
#  Mapping Latin-based characters to the Arabic-based equivalents
#==============================================================================
    def _latin2arabic(self, char):
        if(char.lower() != ""):
            if(char.lower() in self.wy_mappings.keys()):
                return self.wy_mappings[char.lower()]
            elif(char.lower() in self.characters_mapping.keys()):
                return self.characters_mapping[char.lower()]
            elif(char.lower() in self.punctuation_mapping):
                return self.punctuation_mapping[char.lower()]
            elif(char.lower() in self.digits_mapping.values()):
                return self.digits_mapping.keys()[self.digits_mapping.values().index(char.lower())]
        return self.UNKNOWN
#==============================================================================
#   
#==============================================================================
if __name__ == "__main__":
    modes = ["-arabic2latin", "-latin2arabic"] # syllable detection not available in the command-line.
    
    arguments = sys.argv[1:]
    mode = sys.argv[1]
    input_file_path = sys.argv[2]
    
    if mode not in modes:
        print "Mode not defined."
        sys.exit(0)
    else:
        file_name = os.path.basename(input_file_path).split(".")[0]
        output_file_name = os.path.dirname(os.path.abspath(input_file_path)) + "/" + file_name+ "_transliterated.txt"
        
        input_file = codecs.open(input_file_path, "r", "utf-8")
        input_text = input_file.read().split("\n")
        output_file = codecs.open(output_file_name, "w", "utf-8")
        transliterated_text = list()
        wergor_transliterator = Wergor(mode)
        for line in input_text:
            line = line.replace(u" و ", u" û ")
            transliterated_line = list()
            line = line.split()
            for token in line:
                trans_token = ""
                try:
                    token = wergor_transliterator._preprocessor(token.lower())
                    tokens_dict = dict()
                    flag = False
                    i = 0
                    for char_index in range(len(token)):
                        if(token[char_index] in wergor_transliterator.digits_mapping.keys() or token[char_index] in wergor_transliterator.digits_mapping.values() or token[char_index] in wergor_transliterator.punctuation_mapping.keys() or token[char_index] in wergor_transliterator.punctuation_mapping.values()):
                            tokens_dict[char_index] = token[char_index]
                            flag = False
                            i = 0
                        elif(token[char_index] in wergor_transliterator.characters_pack[mode] or token[char_index] in wergor_transliterator.target_char or token[char_index] == wergor_transliterator.hemze):
                            if(flag):
                                tokens_dict[char_index-i] =  tokens_dict[char_index-i] + token[char_index]
                            else:
                                tokens_dict[char_index] = token[char_index]
                            flag = True
                            i += 1
                        else:
                            tokens_dict[char_index] = wergor_transliterator.UNKNOWN
                    for token_key in tokens_dict:
                        if(len(tokens_dict[token_key]) >0 ):
                            trans_token = trans_token + wergor_transliterator._transliterate(tokens_dict[token_key])
                except:
                        trans_token = wergor_transliterator.UNKNOWN
                transliterated_line.append(trans_token)
            transliterated_text.append(" ".join(transliterated_line).replace(u" w ", u" û "))
        output_file.write("\n".join(transliterated_text))
