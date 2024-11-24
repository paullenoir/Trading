export interface Tendance {
    id: number;      
    market: string;
    interval_time: string;
    date: string;
    close_price: string;
    pente_EMA20: string;
    pente_EMA50: string;
    pente_EMA200: string;
    tendance_EMA20: string;
    tendance_EMA50: string;
    tendance_EMA200: string;
    tendance_all: string;
}