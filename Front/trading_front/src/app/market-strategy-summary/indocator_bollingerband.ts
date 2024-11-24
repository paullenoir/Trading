export interface IndicatorBollingerBand {
    id: number;      
    market: string;
    interval_time: string;
    date: string;
    close_price: string;
    BB_Lower: string;
    BB_Middle: string;
    BB_Upper: string;
    BB_Bandwidth: string;
    BB_Percent: string;
}