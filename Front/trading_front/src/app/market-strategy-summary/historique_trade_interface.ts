export interface HistoriqueTrade {
    id: number;                   // ID de l'enregistrement
    market: string;               // Nom du marché (ex: "NVDA.NE")
    interval_time: string;        // Intervalle de temps (ex: "1d")
    date_start: string;           // Date de début (ex: "2022-03-23 00:00:00")
    date_end: string;             // Date de fin (ex: "2022-03-31 00:00:00")
    strategyName: string;         // Nom de la stratégie (ex: "Tendance")
    strategyParameter: string;    // Paramètres de la stratégie (ex: "[]")
    buy_price: string;            // Prix d'achat (ex: "6.349999904632568")
    sell_price: string;           // Prix de vente (ex: "6.777500152587891")
    dollars_profit: string;       // Profit en dollars (ex: "0.42750024795532227")
    percent_profit: string;       // Profit en pourcentage (ex: "6.732287470483968")
}