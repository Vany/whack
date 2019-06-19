import { Injectable } from '@angular/core';
import {interval, Observable} from 'rxjs';
import {environment} from '../environments/environment';
import {flatMap} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';

export class Charger {
  name: string;
  price: number;
  latitude: number;
  longitude: number;
}

// @Injectable({
//   providedIn: 'root'
// })

@Injectable()
export class ChargerService {
  chargers: Charger[];

  constructor(private http: HttpClient) { }

  getChargers(): Observable<any> {
      return interval(1000).pipe(flatMap( () => {
        const command = environment.apiUrl;
        return this.http.get(command);
      }));
  }

  parceData(data: any): Charger[] {
    const result: Charger[] = [
        { name: 'charter1', price: 50, latitude: 52.520008, longitude: 13.403954},
      { name: 'charter2', price: 100, latitude: 52.521008, longitude: 13.404954}
    ];

    return result;
  }

}
