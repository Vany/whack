import { Component } from '@angular/core';
import {icon, latLng, marker, tileLayer} from 'leaflet';
import {ChargerService, Charger} from '../charger.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  layers = [];
  options = {
    layers: [
      tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '...' })
    ],
    zoom: 11,
    center: latLng(52.520008, 13.404954),

  };

  constructor(private chargerService: ChargerService) {}

  ngOnInit() {


    this.chargerService.getChargers().subscribe(data => {
      this.showChargers(this.chargerService.parceData(data));
    });

    // this.showChargers(this.chargerService.parceData());

  }

  showChargers(chargers: Charger[]) {
    chargers.map((charger) => {
      const m = marker([charger.latitude, charger.longitude], {
        title: charger.name,
        alt: charger.name,
        clickable: true,
        riseOnHover: true,
        icon: icon({
          iconSize: [ 25, 41 ],
          iconAnchor: [ 13, 41 ],
          iconUrl: 'assets/marker-icon.png',
          shadowUrl: 'assets/marker-shadow.png'
        })
      });

      m.bindPopup('<ion-button size="small" >' + charger.name +  ' price ' + charger.price + '</ion-button>');
      this.layers.push(m);
    });
  }

  click(event) {
    console.log(event);

  }


}
