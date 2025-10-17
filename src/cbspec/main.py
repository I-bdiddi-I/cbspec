import config
import get_data

if __name__ == "__main__":
    #print(config.GENAREA)
    #print(get_data.parquet_file)
    cbdf=get_data.set_up_data_frame([config.CBMCINFILE, config.CBDTINFILE], 'CBSD')
    tadf=get_data.set_up_data_frame([config.TAMCINFILE, config.TADTINFILE], 'TASD')
    print(cbdf,tadf)