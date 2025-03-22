import pandas as pd
import yaml
import joblib
import logging
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import PowerTransformer
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression
from pathlib import Path
from sklearn.ensemble import StackingRegressor
from sklearn.pipeline import Pipeline
from sklearn import set_config

# set the transformer outputs to pandas
set_config(transform_output='pandas')

TARGET = "time_taken"

# create logger
logger = logging.getLogger("model_training")
logger.setLevel(logging.INFO)

# console handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# add handler to logger
logger.addHandler(handler)

# create a fomratter
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to handler
handler.setFormatter(formatter)


def load_data(data_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_path)
    
    except FileNotFoundError:
        logger.error("The file to load does not exist")
    
    return df

def read_params(file_path):
    with open(file_path,"r") as f:
        params_file = yaml.safe_load(f)
    
    return params_file


def save_model(model, save_dir: Path, model_name: str):
    # form the save location
    save_location = save_dir / model_name
    # save the model
    joblib.dump(value=model,filename=save_location)
    
    
def save_transformer(transformer, save_dir: Path, transformer_name: str):
    # form the save location
    save_location = save_dir / transformer_name
    # save the transformer
    joblib.dump(transformer, save_location)
    
    
def train_model(model, X_train: pd.DataFrame, y_train):
    # fit on the data
    model.fit(X_train,y_train)
    return model


def make_X_and_y(data:pd.DataFrame, target_column: str):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y


def load_preprocessor(file_path: Path):

    preprocessor = joblib.load(file_path)

    return preprocessor



if __name__ == "__main__":
    # root path
    root_path = Path(__file__).parent.parent.parent
    # train data load path
    data_path_precessed = root_path / "data" / "processed" / "train_trans.csv"
     # train data load path before transformation
    data_path_intrim = root_path / "data" / "interim" / 'train.csv'
    #preprocessor path
    preprocessor_path = root_path / "models" / "preprocessor.joblib"
    # parameters file
    params_file_path = root_path / "params.yaml"
    
    # load the training data
    training_data = load_data(data_path_intrim)
    logger.info("Training Data without transformation read successfully")
    
    # split the data into X and y
    X_train, y_train = make_X_and_y(training_data, TARGET)
    logger.info("Dataset splitting completed")

    #loading the preprocessor
    preprocessor = load_preprocessor(preprocessor_path)
    
    # model parameters
    model_params = read_params(params_file_path)['Train']
    
    # rf_params
    rf_params = model_params['Random_Forest']
    logger.info("random forest parameters read")
    
    # build random forest model
    rf = RandomForestRegressor(**rf_params)
    logger.info("built random forest model")
    
    # light gbm params
    lgbm_params = model_params["LightGBM"]
    logger.info("Light GBM parameters read")

    # build light gbm model
    lgbm = LGBMRegressor(**lgbm_params)
    logger.info("built Light GBM model")
    
    # meta model
    lr = LinearRegression()
    logger.info("Meta model built")
    
    # power transformer
    power_transform = PowerTransformer()
    logger.info("Target Transformer built")


    #lgbm Base estimator skleran pipeline
    lgbm_pipeline = Pipeline([('preprocess_data',preprocessor),
                              ('lgbm_regressor',lgbm)])
    logger.info("light_gbm pipeline built")


    #RF Base estimator skleran pipeline
    RF_pipeline = Pipeline([('preprocess_data',preprocessor),
                              ('RF_regressorr',rf)])
    logger.info("Random_forest pipeline built")


    

    # form the stacking regressor
    stacking_reg = StackingRegressor(estimators=[("rf_model",RF_pipeline),
                                                 ("lgbm_model",lgbm_pipeline)],
                                     final_estimator=lr,
                                     cv=5,n_jobs=-1)
    logger.info("Stacking regressor built")
    
    # make the model wrapper
    model = TransformedTargetRegressor(regressor=stacking_reg,
                                       transformer=power_transform)
    logger.info("Models wrapped inside wrapper")
    
    # fit the model on training data
    train_model(model,X_train,y_train)
    logger.info("Model training completed")
    
    # model name
    model_filename = "model.joblib"
    # directory to save model
    model_save_dir = root_path / "models"
    model_save_dir.mkdir(exist_ok=True)
    
    # extract the model from wrapper
    stacking_model = model.regressor_
    transformer = model.transformer_

    # save the model
    save_model(model=model,
            save_dir=model_save_dir,
            model_name=model_filename)
    logger.info("Trained model saved to location")
    
    # save the stacking model
    stacking_filename = "stacking_regressor.joblib"
    save_model(model=stacking_model,
            save_dir=model_save_dir,
            model_name=stacking_filename)
    logger.info("Trained model saved to location")
    
    # save the transformer
    transformer_filename = "power_transformer.joblib"
    transformer_save_dir = model_save_dir
    save_transformer(transformer, transformer_save_dir, transformer_filename)
    logger.info("Transformer saved to location")