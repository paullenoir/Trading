export interface MarketSummary {
    id: string;
    name: string;
    date: string;
    interval_time: string;
    inTrading: string;
    buyPrice: string;
    currentPrice: string;
    strategySummaryColor: string;
    strategy_tendance_color: string;
    strategy_macd_color: string;
    strategy_ichimoku_color: string;
    strategy_2sma_color: string;
    strategy_bb_color: string;
    strategy_rsi_color: string;
    strategy_stochastic_color: string;
    
}

// Enum pour limiter les valeurs des couleurs possibles
// export enum StrategyColor {
//     Red = 'red',
//     Green = 'green'
// }

// Interface pour regrouper les couleurs des différentes stratégies
// export interface StrategyColors {
//     tendance: StrategyColor;
//     macd: StrategyColor;
//     ichimoku: StrategyColor;
//     sma2: StrategyColor;
//     bb: StrategyColor;
//     rsi: StrategyColor;
//     stochastic: StrategyColor;
// }
