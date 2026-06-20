# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

# List of assets simulated by the engine
ASSET_CONFIG = {
    # Cryptocurrencies
    "BTC": {"name": "Bitcoin", "type": "CRYPTO", "start_price": 65000.0, "volatility": 0.05, "yf_ticker": "BTC-USD"},
    "ETH": {"name": "Ethereum", "type": "CRYPTO", "start_price": 3500.0, "volatility": 0.06, "yf_ticker": "ETH-USD"},
    "SOL": {"name": "Solana", "type": "CRYPTO", "start_price": 140.0, "volatility": 0.08, "yf_ticker": "SOL-USD"},
    # Stocks
    "AAPL": {"name": "Apple Inc.", "type": "STOCK", "start_price": 180.0, "volatility": 0.02, "yf_ticker": "AAPL"},
    "TSLA": {"name": "Tesla Inc.", "type": "STOCK", "start_price": 175.0, "volatility": 0.04, "yf_ticker": "TSLA"},
    "NVDA": {"name": "NVIDIA Corp.", "type": "STOCK", "start_price": 850.0, "volatility": 0.05, "yf_ticker": "NVDA"},
    # Forex
    "EURUSD": {"name": "EUR / USD", "type": "FOREX", "start_price": 1.08, "volatility": 0.005, "yf_ticker": "EURUSD=X"},
    "USDJPY": {"name": "USD / JPY", "type": "FOREX", "start_price": 155.0, "volatility": 0.006, "yf_ticker": "JPY=X"},
    "GBPUSD": {"name": "GBP / USD", "type": "FOREX", "start_price": 1.25, "volatility": 0.005, "yf_ticker": "GBPUSD=X"}
}

# Financial settings
INITIAL_CASH = 10000.0
LEVERAGE_OPTIONS = [1, 2, 5, 10, 25, 50]
MAINTENANCE_MARGIN = 0.15  # Liquidate if margin equity drops below 15% of initial margin
TRANSACTION_FEE = 0.001   # 0.1% transaction fee

# Staking yield rate (per game tick)
STAKING_YIELD_RATE = 0.001

# Bank loan settings
LOAN_INTEREST_RATE = 0.005  # 0.5% per tick
DEBT_REPOSSESSION_RATIO = 1.5 # Repossess assets if outstanding debt exceeds 150% of net worth

# Monthly Expenses settings
EXPENSE_INTERVAL_TICKS = 30
EXPENSE_AMOUNT = 1500.0

# Progression ranks based on Net Worth
PROGRESSION_RANKS = [
    (0.0, "Broke Retailer"),
    (5000.0, "Retail Hustler"),
    (25000.0, "Prop Trader"),
    (100000.0, "Whale"),
    (1000000.0, "Financial Institution")
]

# Luxury shop inventory
LUXURY_SHOP = {
    "rolex": {"name": "Rolex Daytona", "cost": 15000.0, "rep": 50},
    "porsche": {"name": "Porsche 911 GT3 RS", "cost": 180000.0, "rep": 600},
    "yacht": {"name": "SuperYacht Horizon", "cost": 1200000.0, "rep": 5000}
}

# Exactly 100 unique fake news events. Do not truncate.
NEWS_FEED = [
    "Elon Musk tweets a picture of a dog eating instant noodles; dog-themed coins pump 400%.",
    "Jerome Powell seen buying a laser eye pin; rate cut rumors surge.",
    "Apple rumors suggest integration of Bitcoin into Apple Pay next month.",
    "Rogue AI bot liquidates its entire blue-chip portfolio by accident.",
    "Major crypto exchange suffers a 2-hour outage; users blame solar flares.",
    "European Central Bank cuts interest rates by 25bps, citing 'vibes'.",
    "Satoshi Nakamoto's wallet wakes up after 12 years; market panics.",
    "Wall Street intern buys wrong ticker; sparks massive short squeeze.",
    "Securities commission launches probe into cat-themed meme coin.",
    "Sudden internet blackout in mining hub causes global hash rate drop.",
    "Rumor: Amazon to accept Dogecoin for AWS billing starting Monday.",
    "A major sovereign wealth fund quietly accumulates Ethereum.",
    "Tech giant announces AI chips that mine crypto while rendering video.",
    "Macro strategist warns of 'hyper-inflationary super-cycle' on TV.",
    "Decentralized exchange hacked for $50M; hacker promises to return half.",
    "Rumors: SEC Commissioner seen drinking coffee from a Bitcoin mug.",
    "A massive whale transfers $1B in BTC to an unknown cold wallet.",
    "Billionaire investor calls crypto 'rat poison squared' again.",
    "Tech startup launches satellite to host space-based nodes.",
    "Central bank digital currency test fails due to database timeout.",
    "Legendary trader tweets 'It is over', causing a 5% sudden dip.",
    "Game development studio adopts Solana for in-game skin economy.",
    "Rumor: Tesla sells remaining Bitcoin; panic selling ensues.",
    "New legislation proposes tax exemption for micro-crypto transactions.",
    "Crypto exchange CEO steps down to pursue full-time meme creation.",
    "Venture capital firm raises $10B fund dedicated to Web3 gaming.",
    "Popular trading app goes down during high volatility; users outraged.",
    "Hardware wallet manufacturer reports a major shipping delay.",
    "Cybersecurity firm discovers malware targeting DeFi browser extensions.",
    "Famous musician releases album exclusively as an Ethereum NFT.",
    "Major bank launches custody service for high-net-worth clients.",
    "Regulators approve first leveraged Ethereum futures ETF.",
    "Sovereign nation adopts Bitcoin as co-legal tender in surprise move.",
    "AI model claims it can predict stock prices with 99% accuracy.",
    "Crypto influencer arrested for promoting rug-pull token.",
    "Rumors: Microsoft is developing a decentralized identity system.",
    "Global logistics firm integrates blockchain to track cargo ships.",
    "Decentralized autonomous organization votes to buy a professional sports team.",
    "Ethereum gas fees hit multi-year lows; traders celebrate.",
    "Mining company buys green energy farm to power operations.",
    "Wall Street firm claims Bitcoin fair value is $200,000.",
    "Tech CEO loses private keys to $100M portfolio in a landfill.",
    "Popular meme coin hits new all-time high, surpassing major banks.",
    "Privacy coin delisted from top exchanges due to compliance concerns.",
    "DeFi protocol collateralized by real-world real estate goes live.",
    "Central bank announces pilot for digital currency offline payments.",
    "Global chip shortage hits mining rig manufacturers hard.",
    "A popular tech blog claims Web3 is dead; market rallies anyway.",
    "Billionaire hedge fund manager reveals 5% personal allocation to BTC.",
    "Major coffee chain begins accepting stablecoin payments in US.",
    "Tax authority issues new guidance on crypto staking rewards.",
    "Crypto gaming platform hosts virtual concert with 1M attendees.",
    "Decentralized storage network passes 10 exabytes of data stored.",
    "Vulnerability found in popular smart contract library; patched in minutes.",
    "Decentralized oracle network reports incorrect data feed due to glitch.",
    "Online brokerage reports record number of new active accounts.",
    "Rumors: Apple working on a hardware wallet built into iPhone.",
    "Top tier investment bank declares inflation has peaked.",
    "Major payment processor processes $100B in stablecoin transactions.",
    "Crypto native browser reaches 50 million active users.",
    "Tech giant announces major layoffs; tech stocks pump on efficiency.",
    "Sovereign nation builds geothermal plant dedicated to green mining.",
    "Decentralized insurance protocol pays out first multi-million claim.",
    "Crypto startup raises $50M in seed round led by elite VC.",
    "SEC delays decision on spot ETF applications again; markets flat.",
    "A localized power outage shuts down a key stock exchange floor.",
    "Global bank says tokenized assets will hit $16T by 2030.",
    "DeFi lending platform hits record $10B in total value locked.",
    "Autonomous vehicle company integrates crypto wallets into cars.",
    "Rumor: Google Cloud to run validators on major Layer 1 network.",
    "Major stablecoin issuer reports 100% backing by US Treasuries.",
    "New browser extension blocks all crypto ads, boosting privacy.",
    "Billionaire says fiat currency is a 'melting ice cube' on live TV.",
    "Decentralized social media app reaches 10 million active profiles.",
    "Top university opens blockchain research center with $20M grant.",
    "Venture capitalist predicts Bitcoin will hit $1M in 90 days.",
    "Exchange token spikes after announcing weekly burning program.",
    "Major fast food chain launches digital collectible loyalty program.",
    "Cyber attackers demand ransom in privacy-focused cryptocurrency.",
    "Decentralized video platform reports exponential creator growth.",
    "Sovereign wealth fund analyst suggests buying high-yield assets.",
    "Global standard body releases framework for tokenized bonds.",
    "Decentralized identity app launched to combat deepfake profiles.",
    "Online retail giant denies rumors of integrating crypto payments.",
    "DeFi project migrates to custom layer-2 subnet for lower fees.",
    "Hardware manufacturer releases liquid-cooled ASIC miner.",
    "Securities regulator issues warning against copy-trading apps.",
    "Investment advisor claims 'cash is king' during market correction.",
    "Crypto donation drive raises $10M for global relief efforts.",
    "Major energy supplier partners with green Bitcoin miner.",
    "Decentralized domain service reports record-breaking domain sales.",
    "Financial media outlet reports retail trading volume hits record highs.",
    "Rumors: Apple to allow third-party app stores with crypto support.",
    "Tech giant integrates AI assistant with decentralized wallet API.",
    "Global financial platform launches zero-fee stablecoin transfers.",
    "Major exchange announces expansion into institutional custody.",
    "DeFi protocol introduces automated yields based on gas fees.",
    "Web3 foundation awards $10M in grants to privacy researchers.",
    "Crypto payment gateway reports 300% year-on-year merchant growth.",
    "Sovereign nation plans to issue tokenized sovereign green bonds."
]