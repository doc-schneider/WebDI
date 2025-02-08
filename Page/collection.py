from dash import html, Input, Output, State, ctx, ALL, callback, dcc

from Views.Collection import CollectionViewer
from DataStructures.TableTypes import TableType
import config

'''
- xyz
'''

def init_Collection(data_table, filter_table=None):
    CollectionView = CollectionViewer(data_table, filter_table)
    CollectionView.sort()
    return CollectionView



