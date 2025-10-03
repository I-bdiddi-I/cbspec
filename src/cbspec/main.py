import config
import get_data

if __name__ == "__main__":
    print(config.GENAREA)
    #print(get_data.parquet_file)
    df=get_data.set_up_data_frame(get_data.parquet_file)
    print("S800 PRINT:",df['s800'])