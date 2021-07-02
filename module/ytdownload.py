from youtube_dl import YoutubeDL
import re

# 7-bit C1 ANSI sequences
ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)

def youtube(link):
    opt = {'quiet': True }
    direkget = YoutubeDL(opt)
    try:
        result = direkget.extract_info(link, download=False)
        result["error"] = False
        return result
    except Exception as e:
        result = ansi_escape.sub('', str(e))
        error = {'error': True, 'Reason': result.split(';')[0]}
        return error