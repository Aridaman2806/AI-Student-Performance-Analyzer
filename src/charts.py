import matplotlib.pyplot as plt

def plot_accuracy_by_chapter(df, output_path):
    # Filter attempted questions only
    attempted = df[df['status'].isin(['answered', 'answeredReview', 'markedReview'])]
    if attempted.empty:
        print("No attempted questions to plot.")
        return
    acc = attempted.groupby('chapter')['is_correct'].mean() * 100
    acc = acc.sort_values(ascending=False)
    plt.figure(figsize=(8, 4))
    acc.plot(kind='bar', color='skyblue')
    plt.title('Accuracy by Chapter')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Chapter')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_time_vs_accuracy(df, output_path):
    attempted = df[df['status'].isin(['answered', 'answeredReview', 'markedReview'])]
    if attempted.empty:
        print("No attempted questions to plot.")
        return
    grouped = attempted.groupby('chapter').agg({'time_taken':'mean', 'is_correct':'mean'})
    plt.figure(figsize=(6, 4))
    plt.scatter(grouped['time_taken'], grouped['is_correct']*100, color='orange')
    for i, txt in enumerate(grouped.index):
        plt.annotate(txt, (grouped['time_taken'].iloc[i], grouped['is_correct'].iloc[i]*100))
    plt.xlabel('Average Time Taken (s)')
    plt.ylabel('Accuracy (%)')
    plt.title('Time vs Accuracy by Chapter')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
