import pandas as pd
from typing import List


def _sort_on(frame):
    _, shape = frame
    rows, _ = shape
    return rows


def _clip_values(df_to_be_clipped, df_to_clip_to):
    return df_to_be_clipped[df_to_be_clipped.index <= df_to_clip_to.last_valid_index()]


def clip_values(dfs: List[pd.DataFrame]):
    index, _ = min(enumerate([frame.shape for frame in dfs]), key=_sort_on)
    return [_clip_values(frame, dfs[index]) for frame in dfs]
