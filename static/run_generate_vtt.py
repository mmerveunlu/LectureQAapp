# This file contains functions to generate
# vtt files from given text file
# Text file format:
#     uttID-index reference_transcription
#

from webvtt import WebVTT, Caption
import datetime
import re
UTTID = r"ENG_[0-9\_]*\_ch[0-9]*_[0-9]*"

def open_text(text):
    """ 
    opens the given file, returns its content
    @text: string, the path of the file 
    returns: 
        a list of string
    """
    with open(text) as fp:
        return fp.readlines()


def parse_text(lines):
    """ 
    processes the given text, returns parsed lines 
    @lines: list of string, each element starts 
       with uttID followed by transcriptions 
       ex:   
       ENG_001_20151602_01204_ch01_0-0001 hi everyone welcome to signals and systems course
    returns: 
    @utt_dict: dictionary, keys are uttID, values are list of transcriptions
    """
    utt_dict = {}
    for line in lines:
        # find the uttID
        uttId = re.findall(UTTID,line)
        if len(uttId) == 0 :
            return "Error UttID not found"
        else:
            uttId = uttId[0]
            # get the reference transcription
            # it starts with 4 digits number + text
            # like -0001 hi!
            text = re.split(UTTID, line)[1]
            if uttId in utt_dict.keys():
                # add the text, remove the digits
                # text starts from 5th place
                utt_dict[uttId].append(text[6:])
            else:
                utt_dict[uttId] = [text[6:]]
    print("There are %d numbers of different utterance IDs in text" %(len(utt_dict)))
    return utt_dict

def parse_segments(segments):
    """
    processes the given segment into dict
    @segments: list of string, eachs element starts with uttID 
       followed by uttID and timings
       ex: 
       ENG_001_20151602_01204_ch01_0-0001 ENG_001_20151602_01204_ch01_0 4.442 8.658
    returns:
    @utt_dict: dictionary, keys are uttID, values are the timings 
    """
    utt_dict = {}
    # check if files contain the same number of transcriptions
    for line in segments:
        uttId = re.findall(UTTID,line)
        if len(uttId) == 0 :
            return "Error UttID not found"
        else:
            # uttId is found
            uttId = uttId[0]
            timings = re.split(UTTID, line)[2]
            if uttId in utt_dict.keys():
                utt_dict[uttId].append(timings)
            else:
                utt_dict[uttId]=[timings]
    print("There are %d numbers of different utterance IDs in the segments" %(len(utt_dict)))
    return utt_dict

def generate_vtt(segments, captions):
    """
    generates vtt formatted captions
    @segments: dict, keys are uttIDs and values are timings 
    @captions: dict, keys are uttIDs and values are captions
    returns 
       None, 
       saves the captions into file named uttID.en.vtt
    """
    for kId,segment in segments.items():
        print("For Lecture %s" %(kId))
        text_vtt = "WEBVTT\nKind: captions\nLanguage: en\n \n"
        # get the text 
        text = captions[kId]
        # check the length of the two lists
        assert len(text)==len(segment)
        for i in range(len(text)):
            # take the time and return as start-->end
            start_str, end_str = transform_timings(segment[i].split())
            text_vtt += start_str +" --> "+ end_str + "\n"
            text_vtt += text[i] + "\n"
        # save the captions with name of the lecture
        with open(kId+".en.vtt","w") as fp:
            fp.write(text_vtt)
    # print(text_vtt)
    return

def generate_vtt_webvtt(segments,captions):
    """
    generates vtt formatted captions using WEbVTT library
    @segments: dict, keys are uttIDs and values are timings 
    @captions: dict, keys are uttIDs and values are captions
    returns 
       None, 
       saves the captions into file named uttID.en.vtt
    """
    for kId,segment in segments.items():
        print("For Lecture %s" %(kId))
        vtt = WebVTT()
        # get the text 
        text = captions[kId]
        # check the length of the two lists
        assert len(text)==len(segment)
        for i in range(len(text)):
            # take the time and return as start-->end
            start_str, end_str = transform_timings(segment[i].split())
            caption = Caption(
                start_str,
                end_str,
                text[i]
            )
            vtt.captions.append(caption)
        # save the captions with name of the lecture
        vtt.save(kId+".en.vtt")
    # print(text_vtt)
    return
    

def transform_timedelta(time, addtime=0):
    """ 
    takes time string, returns vtt formatted time 
    @time: string, ex: 305.805 
    @addtime: int, additional seconds to be added
    returns: 
      HH:MM:SS.ss formatted time
      ex: 00:05:05.805
    """ 
    seconds, mseconds = time.split(".") 
    mseconds = float(mseconds) + 1000 * (float(seconds)+addtime)
    hours, mseconds = divmod(mseconds,3600000)
    minutes, mseconds = divmod(mseconds, 60000)
    seconds = float(mseconds) / 1000
    str_dt = ("%02i:%02i:%06.3f" % (hours, minutes, seconds))
    return str_dt

def transform_timings(times):
    """takes timing strings and return as vtt format timing """
    # add_time = datetime.timedelta(seconds=10)
    # start_str_dt = str(datetime.timedelta(seconds=float(times[0]))+add_time)
    # end_str_dt = str(datetime.timedelta(seconds=float(times[1]))+add_time)
    # return start_str_dt,end_str_dt
    return transform_timedelta(times[0]), transform_timedelta(times[1])
    
def main():
    ftext = "text"
    fsegments = "segments"
    # open the text file
    content = open_text(ftext)
    # parse the text into a dict of utterances
    utt_dict_text = parse_text(content)
    # parse segments
    content = open_text(fsegments)
    utt_dict_segments = parse_segments(content)
    generate_vtt_webvtt(utt_dict_segments, utt_dict_text)
    # generate_vtt(utt_dict_segments,utt_dict_text)

    return


if __name__== "__main__":
    main()

