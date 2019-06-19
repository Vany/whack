import { Injectable } from '@angular/core';
import {interval, Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {flatMap} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';

class Charger {
  owner: string;
  price: number;
  latitude: number;
  longitude: number;
}

@Injectable({
  providedIn: 'root'
})
export class ChargerService {
  chargers: Charger[]

  constructor(private http: HttpClient) { }

  getChargers(): Observable<any> {
    // let a = new Observable<this.chargers>;//.bind(this.alerts);
    // return this.chargers;

      return interval(1000).pipe(flatMap( () => {
        const command = environment.apiUrl + '/chargers';
        return this.http.get(command);
      }));
  }

}
