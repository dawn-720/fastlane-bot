# ------------------------------------------------------------
# Auto generated test file `test_043_TestEmptyCarbonOrders.py`
# ------------------------------------------------------------
# source file   = NBTest_043_TestEmptyCarbonOrders.py
# test id       = 043
# test comment  = TestEmptyCarbonOrders
# ------------------------------------------------------------



"""
This module contains the tests for the exchanges classes
"""
from fastlane_bot import Bot, Config
from fastlane_bot.bot import CarbonBot
from fastlane_bot.tools.cpc import ConstantProductCurve
from fastlane_bot.tools.cpc import ConstantProductCurve as CPC
from fastlane_bot.events.exchanges import UniswapV2, UniswapV3, SushiswapV2, CarbonV1, BancorV3
from fastlane_bot.events.interface import QueryInterface
from fastlane_bot.helpers.poolandtokens import PoolAndTokens
from fastlane_bot.helpers import TradeInstruction, TxReceiptHandler, TxRouteHandler, TxSubmitHandler, TxHelpers, TxHelper
from fastlane_bot.events.managers.manager import Manager
from fastlane_bot.events.interface import QueryInterface
from joblib import Parallel, delayed
from dataclasses import dataclass, asdict, field
import pytest
import math
import json
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CPC))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(Bot))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(UniswapV2))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(UniswapV3))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(SushiswapV2))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(CarbonV1))
print("{0.__name__} v{0.__VERSION__} ({0.__DATE__})".format(BancorV3))
from fastlane_bot.testing import *
from fastlane_bot.modes import triangle_single_bancor3
#plt.style.use('seaborn-dark')
plt.rcParams['figure.figsize'] = [12,6]
from fastlane_bot import __VERSION__
require("3.0", __VERSION__)



C = cfg = Config.new(config=Config.CONFIG_MAINNET)
C.DEFAULT_MIN_PROFIT_BNT = 0.02
C.DEFAULT_MIN_PROFIT = 0.02
cfg.DEFAULT_MIN_PROFIT_BNT = 0.02
cfg.DEFAULT_MIN_PROFIT = 0.02
assert (C.NETWORK == C.NETWORK_MAINNET)
assert (C.PROVIDER == C.PROVIDER_ALCHEMY)
setup_bot = CarbonBot(ConfigObj=C)
pools = None
with open('fastlane_bot/data/tests/latest_pool_data_testing.json') as f:
    pools = json.load(f)
pools = [pool for pool in pools]
pools[0]
static_pools = pools
state = pools
exchanges = list({ex['exchange_name'] for ex in state})
db = QueryInterface(state=state, ConfigObj=C, exchanges=exchanges)
setup_bot.db = db

static_pool_data_filename = "static_pool_data"

static_pool_data = pd.read_csv(f"fastlane_bot/data/{static_pool_data_filename}.csv", low_memory=False)
    
uniswap_v2_event_mappings = pd.read_csv("fastlane_bot/data/uniswap_v2_event_mappings.csv", low_memory=False)
        
tokens = pd.read_csv("fastlane_bot/data/tokens.csv", low_memory=False)
        
exchanges = "carbon_v1,bancor_v3,uniswap_v3,uniswap_v2,sushiswap_v2"

exchanges = exchanges.split(",")


alchemy_max_block_fetch = 20
static_pool_data["cid"] = [
        cfg.w3.keccak(text=f"{row['descr']}").hex()
        for index, row in static_pool_data.iterrows()
    ]
static_pool_data = [
    row for index, row in static_pool_data.iterrows()
    if row["exchange_name"] in exchanges
]

static_pool_data = pd.DataFrame(static_pool_data)
static_pool_data['exchange_name'].unique()
mgr = Manager(
    web3=cfg.w3,
    cfg=cfg,
    pool_data=static_pool_data.to_dict(orient="records"),
    SUPPORTED_EXCHANGES=exchanges,
    alchemy_max_block_fetch=alchemy_max_block_fetch,
    uniswap_v2_event_mappings=uniswap_v2_event_mappings,
    tokens=tokens.to_dict(orient="records"),
)

start_time = time.time()
Parallel(n_jobs=-1, backend="threading")(
    delayed(mgr.add_pool_to_exchange)(row) for row in mgr.pool_data
)
cfg.logger.info(f"Time taken to add initial pools: {time.time() - start_time}")

mgr.deduplicate_pool_data()
cids = [pool["cid"] for pool in mgr.pool_data]
assert len(cids) == len(set(cids)), "duplicate cid's exist in the pool data"
def init_bot(mgr: Manager) -> CarbonBot:
    """
    Initializes the bot.

    Parameters
    ----------
    mgr : Manager
        The manager object.

    Returns
    -------
    CarbonBot
        The bot object.
    """
    mgr.cfg.logger.info("Initializing the bot...")
    bot = CarbonBot(ConfigObj=mgr.cfg)
    bot.db = db
    bot.db.mgr = mgr
    assert isinstance(
        bot.db, QueryInterface
    ), "QueryInterface not initialized correctly"
    return bot
bot = init_bot(mgr)
bot.db.handle_token_key_cleanup()
bot.db.remove_unmapped_uniswap_v2_pools()
bot.db.remove_zero_liquidity_pools()
bot.db.remove_unsupported_exchanges()
tokens = bot.db.get_tokens()
ADDRDEC = {t.key: (t.address, int(t.decimals)) for t in tokens if not math.isnan(t.decimals)}
flashloan_tokens = bot.setup_flashloan_tokens(None)
CCm = bot.setup_CCm(None)
pools = db.get_pool_data_with_tokens()

arb_mode = "multi"


# ------------------------------------------------------------
# Test      043
# File      test_043_TestEmptyCarbonOrders.py
# Segment   Test_Empty_Carbon_Orders_Removed
# ------------------------------------------------------------
def test_test_empty_carbon_orders_removed():
# ------------------------------------------------------------
    
    # +
    arb_finder = bot._get_arb_finder("multi")
    finder = arb_finder(
                flashloan_tokens=flashloan_tokens,
                CCm=CCm,
                mode="bothin",
                result=arb_finder.AO_CANDIDATES,
                ConfigObj=bot.ConfigObj,
            )
    r = finder.find_arbitrage()
    
    (
                best_profit,
                best_trade_instructions_df,
                best_trade_instructions_dic,
                best_src_token,
                best_trade_instructions,
            ) = r[11]
            
    best_trade_instructions_dic
    # Check that this gets filtered out
    test_trade = [{'cid': '0x36445535fc762f6c53277a667500a41e31b51bec800e76aab33dafab75da4eaa',
      'tknin': 'WBTC-C599',
      'amtin': 0.008570336169213988,
      'tknout': 'WETH-6Cc2',
      'amtout': -0.13937506393995136,
      'error': None},
     {'cid': '9187623906865338513511114400657741709420-1',
      'tknin': 'WETH-6Cc2',
      'amtin': 0,
      'tknout': 'WBTC-C599',
      'amtout': 0,
      'error': None},
     {'cid': '9187623906865338513511114400657741709458-1',
      'tknin': 'WETH-6Cc2',
      'amtin': 0.13937506393995136,
      'tknout': 'WBTC-C599',
      'amtout': 0.008870336169213988,
      'error': None}]
    
    (
    ordered_trade_instructions_dct,
    tx_in_count,
    ) = bot._simple_ordering_by_src_token(
    test_trade, best_src_token
    )
    ordered_scaled_dcts = bot._basic_scaling(
                ordered_trade_instructions_dct, best_src_token
            )
    ordered_trade_instructions_objects = bot._convert_trade_instructions(ordered_scaled_dcts)
    tx_route_handler = bot.TxRouteHandlerClass(
                trade_instructions=ordered_trade_instructions_objects
            )
    agg_trade_instructions = (
                tx_route_handler.aggregate_carbon_trades(ordered_trade_instructions_objects)
                if bot._carbon_in_trade_route(ordered_trade_instructions_objects)
                else ordered_trade_instructions_objects
            )
    # Calculate the trade instructions
    calculated_trade_instructions = tx_route_handler.calculate_trade_outputs(
        agg_trade_instructions
    )
    encoded_trade_instructions = tx_route_handler.custom_data_encoder(
                calculated_trade_instructions
            )
    deadline = bot._get_deadline()
    
    # Get the route struct
    route_struct = [
        asdict(rs)
        for rs in tx_route_handler.get_route_structs(
            encoded_trade_instructions, deadline
        )
    ]
    for route in route_struct:
        if route["platformId"] == 6:
            encoded_trade = route["customData"].split("0x")[1]
            encoded_trades = [encoded_trade[i:i+64] for i in range(0, len(encoded_trade), 64)]
            for trade in encoded_trades:
                assert trade != "0000000000000000000000000000000000000000000000000000000000000000", f"[TestEmptyCarbonOrders] Empty Carbon instructions not filtered out by calculate_trade_outputs"