import { HomeComponent } from './home/home.component';
import { KinesisHelperComponent } from './kinesis-helper/kinesis-helper.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
    { path: '', component: KinesisHelperComponent },
    { path: 'kinesis-helper', component: KinesisHelperComponent },
    { path: '**', redirectTo: '' }
    
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
