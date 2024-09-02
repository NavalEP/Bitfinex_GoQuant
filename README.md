
# Bitfinex Tool

It is a command-line tool designed to interact with the Bitfinex API, allowing users to place orders, modify orders, cancel orders, retrieve active orders, and retrieve positions.




## Authors

- [@Naval](https://github.com/NavalEP)


## Installation

Install Required Packages: Make sure to have the required Python packages installed. You can do this using `pip`:

```bash
  pip install -r requirements.txt
```
    

## Environment Variables

Create a .env file in the same directory as main.py with your Bitfinex API key and secret:

`BITFINEX_API_KEY`
`BITFINEX_API_SECRET`

## Usage/Examples

### General Help
To display the general help menu, showing all available commands:

```
python main.py -h
```

### Place Order

To place a new order, use command `p`. You need to specify the amount and price for the order.

##### Help for Place Order:
```
python main.py p -h

```

##### Example:
```
python main.py p --amount 0.1 --price 10000
```

### Get Orders
To retrieve all active orders, use  `g`.

```
python main.py g

```

### Modify Order
To modify an existing order, use the `m`. You need to provide the `order_id`, `new_amount`, and `new_price`.

```
python main.py m --order_id 1725291966 --new_amount 0.2 --new_price 10500

```

### Cancel Order
To cancel an existing order, use command `c`. You need to provide the order_id.

```
python main.py c --order_id 1725292034821

```

### Retrieve Positions
To retrieve all positions, use command `rp`.

```
python main.py rp

```

