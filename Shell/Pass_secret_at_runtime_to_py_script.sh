& {Set-Item Env:my_password  "yoUr_str0Ng_paSswoRd_heRe"} | py myscript.py

# Your Python script must contain the following:
# import os
# my_password = os.getenv('my_password')