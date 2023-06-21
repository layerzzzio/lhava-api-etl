# Welcome to my LLAVA blockchain etl

I am Loïc, currently working out of Durham, UK.

Here is my take on the assignment aiming to fetch data from the Solana blockchain. You will find most of the code in the main.py, the blockchain module and utils.py.

## tldr: How to execute the code & see the results
To run the ETL (it is also explained in the [collaboration.md](collaboration.md)) just type the following command, at the root of the project, from a MacOS or Linux terminal:
```
python main.py blockchain Solana <MINT_KEY>
```

Example with mint key `CqR9VaK9GQhLqGdf9ZTGpt9vMZ1zEfztKzab2iy1TNzU` from this [Okay Bear NFT](https://magiceden.io/item-details/CqR9VaK9GQhLqGdf9ZTGpt9vMZ1zEfztKzab2iy1TNzU?name=Okay-Bear-%23445)

```
python main.py blockchain Solana CqR9VaK9GQhLqGdf9ZTGpt9vMZ1zEfztKzab2iy1TNzU
```

I created a dashboard POC [here](https://app.cvbuilderai.com/solana) (with Flutter) so you can see the data in realtime:

![dashboard](ressources/dashboard.png)

Note: I created a temporary screen in my application [CVBuilderAI](https://app.cvbuilderai.com/) to do so. Don't be surprised if you see the cvbuilderai URL.

## The rest of the assignment
Also, you will find:

- Part 2 of the assignment is here -> [optimization.md](optimization.md) (eg. how to optimize & troubleshoot it)
- Part 3 of the assignment is here -> [collaboration.md](collaboration.md) (eg. how the ETL works & collaborations)

## Personal note

This was my first experience exploring blockchain data and API, so it's possible that I made some functional errors during the process. I would greatly appreciate any feedback or insights if you notice any irregularities or areas where improvements can be made. Your assistance is highly valued.

## Greetings
Thank you for giving me the opportunity to dive into the blockchain data.
I enjoyed doing so 🤩 

![loic pp](ressources/pp.jpg)
