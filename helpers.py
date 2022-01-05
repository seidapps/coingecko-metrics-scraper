from dataclasses import dataclass, asdict

@dataclass
class CoinMetrics:
    coin_id: str
    coin_name: str
    symbol: str
    price: float
    volume_24h: int
    market_cap: int
    fully_diluted_valuation: int
    circulating_supply: int
    total_supply: int
    max_supply: int
    twitter_followers: int
    facebook_likes: int
    reddit_average_posts_48h: float
    reddit_average_comments_48h: float
    reddit_subscribers: int
    reddit_accounts_active_48h: int
    telegram_channel_user_count: int
    forks: int
    stars: int
    subscribers: int
    total_issues: int
    closed_issues: int
    pull_requests_merged: int
    pull_request_contributors: int
    code_additions_deletions_4_weeks_additions: int
    code_additions_deletions_4_weeks_deletions: int
    commit_count_4_weeks: int

@dataclass
class CoinExchange:
    coin_id: str
    coin_name: str
    symbol: str
    base: str
    target: str
    market_name: str
    market_identifier: str
    market_has_trading_incentive: str
    price: str
    volume: str
    pp_total_volume: str
    is_stale: bool