import { Injectable } from '@angular/core';
import { HttpClient, HttpParams  } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HistoriqueTrade } from "./market-strategy-summary/historique_trade_interface";
import { IndicatorMACD } from "./market-strategy-summary/indicator_macd_interface";
import { MarketPrice } from "./market-strategy-summary/market_price_interface";
import {MarketSummary} from './market-summary/market-summary_interface'
import { IndicatorEMA } from './market-strategy-summary/indicator_ema';
import { Tendance } from './market-strategy-summary/tendance_interface';
import { Indicator2sma } from './market-strategy-summary/indicator_2sma';
import { IndicatorIchimoku } from './market-strategy-summary/indicator_ichimoku';
import { IndicatorRSI } from './market-strategy-summary/indicator_rsi';
import { IndicatorStochastic } from './market-strategy-summary/indicator_stochastic';
import { IndicatorBollingerBand } from './market-strategy-summary/indocator_bollingerband';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // private domain = "http://127.0.0.1:8000/api/"
  private domain = "http://168.138.69.233:8001/api/"

  constructor(private http: HttpClient) { }

  getMarketSummaries(): Observable<MarketSummary[]>{
    const url = `${this.domain}marketstrategyresult/`;
    return this.http.get<MarketSummary[]>(url).pipe(
      map(data =>
        data.map(item => ({
          id: item.id,
          name: item.name,
          date: item.date,
          interval_time: item.interval_time,
          inTrading: "",
          buyPrice: "",
          currentPrice: "",
          strategySummaryColor: "",
          strategy_tendance_color: item.strategy_tendance_color,
          strategy_macd_color: item.strategy_macd_color,
          strategy_ichimoku_color: item.strategy_ichimoku_color,
          strategy_2sma_color: item.strategy_2sma_color,
          strategy_bb_color: item.strategy_bb_color,
          strategy_rsi_color: item.strategy_rsi_color,
          strategy_stochastic_color: item.strategy_stochastic_color
        }))
      )
    );
  }

  getHistoricTrade(market: string, interval: string, strategy: string):Observable<HistoriqueTrade[]> {
    //?market=NVDA.NE&interval_time=1d&strategyName=2MM
    const params = new HttpParams()
      .set('market', market)
      .set('interval_time', interval)
      .set('strategyName', strategy);
    const url = `${this.domain}tradingresults/`;
    return this.http.get<HistoriqueTrade[]>(url, { params }).pipe(
      map(data =>
        data.map(item => ({
          id: item.id,
          market: item.market,
          interval_time: item.interval_time,
          date_start: item.date_start,
          date_end: item.date_end,
          strategyName: item.strategyName,
          strategyParameter: item.strategyParameter,
          buy_price: item.buy_price,
          sell_price: item.sell_price,
          dollars_profit: item.dollars_profit,
          percent_profit: item.percent_profit
        }))
      )
    );
  }

  getMarketPrice(market: string, interval: string): Observable<MarketPrice[]>{
    //marketprices/?market=NVDA.NE&interval_time=1d
    const params = new HttpParams()
    .set('market', market)
    .set('interval_time', interval);
    const url = `${this.domain}marketprices/`;
    return this.http.get<MarketPrice[]>(url, { params }).pipe(
      map(data =>
        data.map(item => ({
          id: item.id,
          market: item.market,
          interval_time: item.interval_time,
          date: item.date,
          low_price: item.low_price,
          high_price: item.high_price,
          open_price: item.open_price,
          close_price: item.close_price,
          adj_close: item.adj_close,
          volume: item.volume
        }))
      )
    );
  }

  getTendance(market: string, interval: string): Observable<Tendance[]>{
    //marketprices/?market=NVDA.NE&interval_time=1d
    const params = new HttpParams()
    .set('market', market)
    .set('interval_time', interval);
    const url = `${this.domain}strategytendances/`;
    return this.http.get<Tendance[]>(url, { params }).pipe(
      map(data =>
        data.map(item => ({
          id: item.id,
          market: item.market,
          interval_time: item.interval_time,
          date: item.date,
          close_price: item.close_price,
          pente_EMA20: item.pente_EMA20,
          pente_EMA50: item.pente_EMA50,
          pente_EMA200: item.pente_EMA200,
          tendance_EMA20: item.tendance_EMA20,
          tendance_EMA50: item.tendance_EMA50,
          tendance_EMA200: item.tendance_EMA200,
          tendance_all: item.tendance_all
        }))
      )
    );
 }

 getIndicatorEMA(market: string, interval: string): Observable<IndicatorEMA[]>{
    //marketprices/?market=NVDA.NE&interval_time=1d
    const params = new HttpParams()
    .set('market', market)
    .set('interval_time', interval);
    const url = `${this.domain}indicatorema/`;
    return this.http.get<IndicatorEMA[]>(url, { params }).pipe(
      map(data =>
        data.map(item => ({
          id: item.id,
          market: item.market,
          interval_time: item.interval_time,
          date: item.date,
          close_price: item.close_price,
          EMA20: item.EMA20,
          EMA50: item.EMA50,
          EMA200: item.EMA200
        }))
      )
    );
  }

  getIndicatorMACD(market: string, interval: string): Observable<IndicatorMACD[]>{
      //marketprices/?market=NVDA.NE&interval_time=1d
      const params = new HttpParams()
      .set('market', market)
      .set('interval_time', interval);
      const url = `${this.domain}indicatormacd/`;
      return this.http.get<IndicatorMACD[]>(url, { params }).pipe(
        map(data =>
          data.map(item => ({
            id: item.id,
            market: item.market,
            interval_time: item.interval_time,
            date: item.date,
            macd: item.macd,
            macd_signal: item.macd_signal,
            macd_histogram: item.macd_histogram,
            close_price: item.close_price
          }))
        )
      );
  }

 getIndicator2MM(market: string, interval: string): Observable<Indicator2sma[]>{
        //indicatorsma/?market=NVDA.NE&interval_time=1d&MM20=&MM_longue=MM200
        const params = new HttpParams()
        .set('market', market)
        .set('interval_time', interval)
        const url = `${this.domain}indicatorsma/`;
        return this.http.get<Indicator2sma[]>(url, { params }).pipe(
          map(data =>
            data.map(item => ({
              ...item,
              close_price: parseFloat(item.close_price as unknown as string),
            }))
          )
        );
 }

 getIndicatorIchimoku(market: string, interval: string): Observable<IndicatorIchimoku[]>{
  const params = new HttpParams()
  .set('market', market)
  .set('interval_time', interval);
  const url = `${this.domain}indicatorichimoku/`;
  return this.http.get<IndicatorIchimoku[]>(url, { params }).pipe(
    map(data =>
      data.map(item => ({
        id: item.id,
        market: item.market,
        interval_time: item.interval_time,
        date: item.date,
        close_price: item.close_price,
        Ichimoku_Conversion: item.Ichimoku_Conversion,
        Ichimoku_Base: item.Ichimoku_Base,
        Ichimoku_LeadingA: item.Ichimoku_LeadingA,
        Ichimoku_LeadingB: item.Ichimoku_LeadingB,
        Ichimoku_Lagging: item.Ichimoku_Lagging
      }))
    )
  );
 }

 getIndicatorRSI(market: string, interval: string): Observable<IndicatorRSI[]>{
  const params = new HttpParams()
  .set('market', market)
  .set('interval_time', interval);
  const url = `${this.domain}indicatorrsi/`;
  return this.http.get<IndicatorRSI[]>(url, { params }).pipe(
    map(data =>
      data.map(item => ({
        id: item.id,
        market: item.market,
        interval_time: item.interval_time,
        date: item.date,
        close_price: item.close_price,
        rsi_7: item.rsi_7,
        rsi_14: item.rsi_14,
        rsi_21: item.rsi_21
      }))
    )
  );
 }

 getIndicatorStochastic(market: string, interval: string): Observable<IndicatorStochastic[]>{
  const params = new HttpParams()
  .set('market', market)
  .set('interval_time', interval);
  const url = `${this.domain}indicatorstochastic/`;
  return this.http.get<IndicatorStochastic[]>(url, { params }).pipe(
    map(data =>
      data.map(item => ({
        id: item.id,
        market: item.market,
        interval_time: item.interval_time,
        date: item.date,
        close_price: item.close_price,
        stochastic_k: item.stochastic_k,
        stochastic_d: item.stochastic_d
      }))
    )
  );
 }

 getIndicatorBollingerBand(market: string, interval: string): Observable<IndicatorBollingerBand[]>{
  const params = new HttpParams()
  .set('market', market)
  .set('interval_time', interval);
  const url = `${this.domain}indicatorbollingerband/`;
  return this.http.get<IndicatorBollingerBand[]>(url, { params }).pipe(
    map(data =>
      data.map(item => ({
        id: item.id,
        market: item.market,
        interval_time: item.interval_time,
        date: item.date,
        close_price: item.close_price,
        BB_Lower: item.BB_Lower,
        BB_Middle: item.BB_Middle,
        BB_Upper: item.BB_Upper,
        BB_Bandwidth: item.BB_Bandwidth,
        BB_Percent: item.BB_Percent,
      }))
    )
  );
 }
}
