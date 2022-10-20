import pandas as pd
import plotly.express as px


def topicModelling():
    tweets_df = pd.read_csv(r'10cluster.csv')
    topics_df = tweets_df[['cluster', 'topic_name']].drop_duplicates().sort_values(by='cluster')
    topics_df.reset_index(inplace=True, drop=True)

    n_topics = len(topics_df)
    user_topic_counts = pd.pivot_table(data=tweets_df,
                                       values='Tweet',
                                       index='Date',
                                       columns='cluster',
                                       aggfunc='count',
                                       fill_value=0)

    user_topic_counts.columns = ['Topic {}'.format(i) for i in range(n_topics)]

    # add column to sum total topics
    user_topic_counts['total_topics'] = user_topic_counts.sum(axis=1)

    # convert topic counts to percentages for each news source
    user_topic_counts_pct = user_topic_counts.apply(lambda x: (x / user_topic_counts['total_topics']))
    user_topic_counts_pct = user_topic_counts_pct.drop(columns=['total_topics'])

    # store value z-values
    z_usr = user_topic_counts_pct.values.tolist()

    # create list of hover text template strings for each z-value in matrix
    topic_names = topics_df.topic_name.tolist()
    hovertext_usr = []
    for yi, yy in enumerate(user_topic_counts_pct.index.tolist()):
        hovertext_usr.append(list())
        for xi, xx in enumerate(topic_names):
            hovertext_usr[-1].append('<b>Topic:</b> {}<br />'
                                     '<b>User:</b> {}<br />'
                                     '<b>Tweet Proportion:</b> {}'.format(xx, yy, z_usr[yi][xi]))

    # plot heatmap
    fig = px.imshow(user_topic_counts_pct,
                    color_continuous_scale="bluyl",
                    width=650,
                    height=500,
                    aspect="auto")

    fig.update_layout(
        margin=dict(l=20,
                    r=0,
                    b=20,
                    t=10,
                    pad=3),
        coloraxis=dict(colorbar=dict(thickness=15,
                                     xpad=2)))

    fig.update_traces(
        hovertemplate=None,  # set this to None in order to use custom hover text
        text=hovertext_usr,
        hoverinfo="text")

    fig.show()
