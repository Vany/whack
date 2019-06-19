import { Component } from '@angular/core';
import {icon, latLng, marker, tileLayer} from 'leaflet';

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

  constructor() {}

  ngOnInit() {
    const m = marker([52.520008, 13.404954], {
      title: 'charger_1',
      alt: 'charger_1',
      clickable: true,
      riseOnHover: true,
      icon: icon({
        iconSize: [ 25, 41 ],
        iconAnchor: [ 13, 41 ],
        iconUrl: 'assets/marker-icon.png',
        shadowUrl: 'assets/marker-shadow.png'
      })
    });

    this.layers.push(m);
  }

  click(event) {
    console.log(event);

    const m = marker([52.530108, 13.404954], {
      title: 'charger_2',
      alt: 'charger_2',
      clickable: true,
      riseOnHover: true,
      icon: icon({
        iconSize: [ 25, 41 ],
        iconAnchor: [ 13, 41 ],
        iconUrl: 'assets/marker-icon.png',
        shadowUrl: 'assets/marker-shadow.png'
      })
    });

    // m.bindPopup('<ion-button size="small" >charge</ion-button>');


    this.layers.push(m);
  }


}
