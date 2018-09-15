# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 21:52:24 2018

@author: fuwen
"""
from pydub import AudioSegment
import os,re,time

def CutMp3(Mp3File):    
    filename = re.findall(r"(.*?)\.mp3|MP3", Mp3File)
    if filename:
        filename[0] += '.mp3'
        mp3 = AudioSegment.from_mp3(Mp3File) 
        mp3 = mp3[30000:len(mp3)-25000]
        mp3.export('cut_'+Mp3File,format="mp3", bitrate="128k")
        
if __name__=='__main__':
    process_start = time.time()
    for Mp3File in os.listdir('.'):
        file_start = time.time()
        CutMp3(Mp3File)
        file_end = time.time()
        print('File %s runs %0.2f seconds.' % (Mp3File, (file_end - file_start)))
    process_end = time.time()
    print('process %s runs %0.2f seconds.' % ('process', (process_end - process_start)))