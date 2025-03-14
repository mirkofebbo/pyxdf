"""
- Timestamps align when synchronize_clocks=True/False.
- original vs. resampled data 
- resampled timestamps are evenly spaced.
- data structure maintained after resampling.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pytest
from pyxdf import load_xdf

path = Path("/home/mirko/Documents/code/Neurolive/example-files")

files = {
    key: path / value
    for key, value in {
        "sine_wave": "sine-2+marker.xdf"
    }.items()
    if (path / value).exists()
}

# open file and visualize the data
streams, header = load_xdf(files["sine_wave"])
print(header["info"]["version"][0] )

for stream in streams:
    y = stream["time_series"]
    print("====================================")
    print("name: ", stream["info"]["name"][0])
    print("type: ", stream["info"]["type"][0])
    print("channel_count: ",stream["info"]["channel_count"][0])
    print("nominal_srate: ", stream["info"]["nominal_srate"][0])
    print("channel_format: ", stream["info"]["channel_format"][0])
    print("created_at: ", stream["info"]["created_at"][0])
    print("desc: ", stream["info"]["desc"][0])
    print("uid: ", stream["info"]["uid"][0])    
    print("PYXDF INFO")
    print("stream_id: ", stream["info"]["stream_id"])
    print("effective_srate: ", stream["info"]["effective_srate"])
    print("segments: ", stream["info"]["segments"])
    print("clock_segments: ", stream["info"]["clock_segments"])
    print("FOOTER INFO")
    print("first_timestamp: ", stream["footer"]["info"]["first_timestamp"][0])
    print("last_timestamp: ", stream["footer"]["info"]["last_timestamp"][0])
    print("sample_count: ", stream["footer"]["info"]["sample_count"][0])
    print("clock_offsets: ", stream["footer"]["info"]["clock_offsets"][0]["offset"][0])
    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream["time_stamps"], y):
            plt.axvline(x=timestamp)
            # print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        # plt.plot(stream["time_stamps"], y)
        print("plotting")
    else:
        raise RuntimeError("Unknown stream format")

# plt.show()


@pytest.mark.parametrize("synchronize_clocks", [False, True])
@pytest.mark.skipif("sine_wave" not in files, reason="Test file not found")
def test_timestamps_alignement(synchronize_clocks):
    path = files["sine_wave"]  
    streams, header = load_xdf(
        path, 
        synchronize_clocks=synchronize_clocks,
    )
    # eeg stream
    # Stream id 3
    assert streams[3]["info"]["type"][0] == "eeg"
    assert streams[4]["info"]["type"][0] == "eeg"
    # Stream id 4




@pytest.mark.parametrize("synchronize_clocks", [False, True])
@pytest.mark.skipif("sine_wave" not in files, reason="Test file not found")
def test_sine_wave_file(synchronize_clocks):
    path = files["sine_wave"]   
    streams, header = load_xdf(
        path, 
        synchronize_clocks=synchronize_clocks,
    )
    assert header["info"]["version"][0] == "1.0"
    # Stream ID: 0
    i = 0
    assert len(streams) == 4
    assert streams[i]["info"]["name"][0] == "ctrl"
    assert streams[i]["info"]["type"][0] == "control"
    assert streams[i]["info"]["channel_count"][0] == "1"
    assert streams[i]["info"]["nominal_srate"][0] == "0.000000000000000"
    assert streams[i]["info"]["channel_format"][0] == "string"
    assert streams[i]["info"]["created_at"][0] == "15415.43635413100"
    desc = streams[i]["info"]["desc"][0]
    assert isinstance(desc, dict), f"Stream {i} desc not a dict {type(desc)}"
    assert streams[i]["info"]["uid"][0] == "3fefaf0e-4732-4a6d-a31d-a4add58890fd"

    # Info added by pyxdf
    assert streams[i]["info"]["stream_id"] == 2
    assert streams[i]["info"]["effective_srate"] == 0
    assert streams[i]["info"]["segments"] == [(0, 0)]
    assert streams[i]["info"]["clock_segments"] == (
        [(0, 0)] if synchronize_clocks else []
    )

    # Footer
    assert streams[i]["footer"]["info"]["first_timestamp"][0] == "15468.027867873"
    assert streams[i]["footer"]["info"]["last_timestamp"][0] == "15468.027867873"
    assert streams[i]["footer"]["info"]["sample_count"][0] == "1"
    first_clock_offset = streams[i]["footer"]["info"]["clock_offsets"][0]["offset"][0]
    assert first_clock_offset["time"][0] == "15466.657564722"
    assert first_clock_offset["value"][0] == "-2.568699983385159e-05"