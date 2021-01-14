import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { KinesisHelperService } from './kinesis-helper.service';
import * as AWS from 'aws-sdk';
import * as uuid from 'uuid';
import { interval } from 'rxjs';

@Component({
  selector: 'app-kinesis-helper',
  templateUrl: './kinesis-helper.component.html',
  styleUrls: ['./kinesis-helper.component.css']
})
export class KinesisHelperComponent implements OnInit {

  @ViewChild('secretAccessKey') secretAccessKey: ElementRef;
  @ViewChild('streamName') streamName: ElementRef;
  @ViewChild('accessKey') accessKey: ElementRef;
  @ViewChild('region') region: ElementRef;

  public isLoadingData: boolean
  public someError: boolean
  public someErrorMessage: String

  public loadingSub;

  public streamingData: String;
  
  constructor(private kinesisServiceHelper: KinesisHelperService) {
    this.isLoadingData = false;
    this.someError = false;
   }

  ngOnInit() {
  }

  public startStream() {

    this.isLoadingData = false;
    this.someError = false;

    const secretAccessKey = this.secretAccessKey.nativeElement.value;
    const streamName = this.streamName.nativeElement.value;
    const accessKey = this.accessKey.nativeElement.value;
    const region = this.region.nativeElement.value;

    if(secretAccessKey === "" || streamName === "" || accessKey === "" || region === "") {
      this.someErrorMessage = "Please enter in all the fields.";
      this.someError = true;
      return;
    }

    this.loadingSub = interval(1000).subscribe(x => {
        this.kinesisServiceHelper.streamData(region, secretAccessKey, accessKey, streamName)
        .subscribe( payload => {
          this.isLoadingData = true;
          this.streamingData = payload;
      }, error => {
          this.isLoadingData = false;
          this.someError = true;
          this.someErrorMessage = error;
          if(this.someErrorMessage == 'NetworkingError: Network Failure') {
            this.someErrorMessage = 'NetworkingError: Stream name and region combination is invalid.'
          }
          this.loadingSub.unsubscribe();
      });
    });
  }

  public stopStream() {
    this.loadingSub.unsubscribe();
    this.isLoadingData = false;
  }

}
