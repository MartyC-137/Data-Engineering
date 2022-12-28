!set variable_substitution=true;
put file://&{csv_path} @~&{stage} auto_compress=true;
