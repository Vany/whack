import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';

import { HomePage } from './home.page';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {ChargerService} from '../charger.service';
import {HttpClient, HttpClientModule} from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    HttpClientModule,
    LeafletModule.forRoot(),
    RouterModule.forChild([
      {
        path: '',
        component: HomePage
      }
    ])
  ],
  declarations: [HomePage],
  providers: [
    ChargerService,
  ]
})
export class HomePageModule {}
