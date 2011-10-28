#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

WORD, COUNT = range(2)

forbidden_words = (
    'about',
    'after',
    'children',
    'other',
    'should',
    'their',
    'there',
    'which',
    'would',
    # 'monday',
    # 'tuesday',
    # 'wednesday',
    # 'thursday',
    # 'friday',
    # 'saturday',
    # 'sunday',
)

    

def bar_chart(data, sample_size=10, xlabel='Word', ylabel='Count', 
              title='Word Usage', bar_width=0.35, legend='CNN', 
              filter_data=True, log=False, color='g'):

    if filter_data:
        data = filter(lambda i: not i[WORD] in forbidden_words, data)

    # Get the most used of the sample size
    sample_data = data[-sample_size:]
    word_counts = [sample[COUNT] for sample in sample_data]


    ind = np.arange(sample_size)  # the x locations for the groups

    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = ax.bar(ind, word_counts, bar_width, color=color, log=log)

    # add some
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind+bar_width)
    ax.set_xticklabels(
        [sample[WORD] for sample in sample_data], 
        rotation=45.0) 

    ax.legend((rects[0],), (legend,), loc=9)


    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')
    
    plt.show()


 
