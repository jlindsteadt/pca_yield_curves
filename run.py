import os
from datetime import datetime as dt

from src.utils import download
from src.rates import clean_rates, maturity_str
from src.pca import PCA
import config as conf

def main():

    if not os.path.exists("assets"):
        os.makedirs("assets")

    download(
        target_path = "assets/data.csv",
        start_date  = conf.start_date,
        end_date    = conf.end_date
    )

    df = clean_rates(
        filepath   = "assets/data.csv", 
        start      = conf.start_date, 
        end        = conf.end_date, 
        maturities = conf.maturities,
        freq       = conf.frequency
    )

    # Train-test split
    test_date = dt.strptime(conf.test_date, "%Y-%m-%d")
    df_train = df[df.index < test_date]
    df_test = df[df.index >= test_date]

    mdl = PCA(df, k=conf.n_components)

    pc_scores      = mdl.eig_scores_k
    pc_vectors     = mdl.eig_vect_k
    pc_vectors_inv = mdl.eig_vect_inv_k
    pc_back_trans  = mdl.yields
    pc_idx         = mdl.idx[:conf.n_components]


if __name__ == "__main__":
    main()