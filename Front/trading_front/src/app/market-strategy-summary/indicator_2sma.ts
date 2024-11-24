export interface Indicator2sma {
    id: number;
    market: string;
    interval_time: string;
    date: string;
    close_price: number; // Le prix de fermeture
    [key: string]: number | string; // Permet des propriétés dynamiques
    // MM10: number;
    // MM15: number;
    // MM20: number;
    // MM25: number;
    // MM30: number;
    // MM35: number;
    // MM40: number;
    // MM45: number;
    // MM50: number;
    // MM55: number;
    // MM60: number;
    // MM65: number;
    // MM70: number;
    // MM75: number;
    // MM80: number;
    // MM85: number;
    // MM90: number;
    // MM95: number;
    // MM100: number;
    // MM200: number;
}
