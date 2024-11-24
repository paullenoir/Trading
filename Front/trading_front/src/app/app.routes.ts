import { Routes } from '@angular/router';
import { MarketSummaryComponent } from './market-summary/market-summary.component';
import { MarketStrategySummaryComponent } from './market-strategy-summary/market-strategy-summary.component';

export const routes: Routes = [
    { path: '', component: MarketSummaryComponent  }, // Route par défaut
    { path: 'strategy/:strategy', component: MarketStrategySummaryComponent }
];
