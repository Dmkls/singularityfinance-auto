
# Singularityfinance testnet auto farm

On chain soft in order to automatically do singularity finance testnet
The software does transactions at random times of the day

![image](https://github.com/user-attachments/assets/d60158f4-7209-47b7-9033-357a49441ecc)

### Features
   - Wrap/unwrap SFI
   - Skate/unstake
   - Claim 
   - Bridge

 ## Quick Star
 1. Install git - [link](https://git-scm.com/downloads)
 2. Press `WIN + R` to open the Run dialog box
 3. Type `cmd` and press enter to open console.
 4. Paste in console `git clone https://github.com/Dmkls/singularityfinance-auto`
 5. Open `singularityfinance-auto` folder and start `INSTALL.bat` to install libraries.
 7. To start soft - `START.bat`

 ## Private keys
 - Paste as many private keys as you want to the `data/private_keys.txt` file

 ## Proxies
 - You need 5 for every 100 accounts. Paste them in `data/proxies.txt` file
 - You don't need a proxy for each account, they are not used for transactions. But are used to get some data to do staking transaction

 ## Settings
 - Open `configs/settings.py`
 - It is a customization file. You can select the transactions that will and will not be done
 - `True`  (or `1`) means to do a transaction
 - `False` (or `0`) means not to do a transaction
 - You can also choose the transaction volume - change the `range` next to the corresponding transaction
