import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score


def save_dataframe_scores(clf, X_test, y_test, experiment_path):
    """Saves dataframe scores in dataframe format

    Args:
        clf: model
        X_test: Feature data for testing
        y_test: Objective feature to inference during testing
        experiment_path: Path used to save this dataframe with scores
    """
    outcomes = {}
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)

    outcomes['acc_score'] = [round(accuracy_score(y_test, y_pred), 3)]
    outcomes['roc_score'] = [round(roc_auc_score(y_test, y_proba, multi_class='ovr'), 3)]

    df = pd.DataFrame(data=outcomes)
    df.to_csv(f'{experiment_path}/scores.csv', storage_options={}, index=False)


def save_plot_feature_importance(clf, X_train, experiment_path):
    """Saves plot with feature importance in an image format

    Args:
        clf: model
        X_train: Feature data for training
        y_test: Objective feature to inference during testing
        experiment_path: Path used to save this image which represents feature importance
    """
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features = X_train.columns[indices]
    importances = importances[indices]

    fig, ax = plt.subplots(figsize=(12, 7))
    plt.barh(range(len(importances)), importances)
    plt.yticks(range(len(importances)), features, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel("Feature importance", fontsize=12)

    plt.savefig(f'{experiment_path}/feature_importance.png')


def save_plot_confusion_matrix(y_test, y_pred, experiment_path):
    """Saves plot with confusion matric in an image format

    Args:
        y_test: Objective feature to inference during testing
        y_pred: Objective feature got from trained model inference
        experiment_path: Path used to save this image which represents confusion matrix
    """
    classes = [0, 1, 2, 3]
    labels = ['low', 'mid', 'high', 'lux']

    c = confusion_matrix(y_test, y_pred)
    c = c / c.sum(axis=1).reshape(len(classes), 1)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(c, annot=True, cmap='BuGn', square=True, fmt='.2f', annot_kws={'size': 10}, cbar=False)
    plt.xlabel('Predicted', fontsize=16)
    plt.ylabel('Real', fontsize=16)
    plt.xticks(ticks=np.arange(0.5, len(classes)), labels=labels, rotation=0, fontsize=12)
    plt.yticks(ticks=np.arange(0.5, len(classes)), labels=labels, rotation=0, fontsize=12)
    plt.title("Simple model", fontsize=18)

    plt.savefig(f'{experiment_path}/confusion_matrix.png')


def save_plot_classification_report(y_test, y_pred, experiment_path):
    """Saves plot with classificataion report in an image format

    Args:
        y_test: Objective feature to inference during testing
        y_pred: Objective feature got from trained model inference
        experiment_path: Path used to save this image which represents classification report
    """
    maps = {'0.0': 'low', '1.0': 'mid', '2.0': 'high', '3.0': 'lux'}

    report = classification_report(y_test, y_pred, output_dict=True)
    df_report = pd.DataFrame.from_dict(report).T[:-3]
    df_report.index = [maps[str(float(i))] for i in df_report.index]

    metrics = ['precision', 'recall', 'support']

    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 7))

    for i, ax in enumerate(axes):
        ax.barh(df_report.index, df_report[metrics[i]], alpha=0.9)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.set_xlabel(metrics[i], fontsize=12)
        ax.invert_yaxis()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.suptitle("Simple model", fontsize=14)
    plt.savefig(f'{experiment_path}/simple_model.png')
