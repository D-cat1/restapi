from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=czcXMSLqoKQ')
aa = yt.streams.filter(progressive=True)

print(aa)