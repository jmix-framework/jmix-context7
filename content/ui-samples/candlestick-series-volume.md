<Path>Add-ons > Charts > Series > Candlestick series > Candlestick series with volume</Path>

CandlestickSeries can be displayed together with a Volume Bar Series, and the axes will be synchronized. Pay attention to the encode property, which indicates what data from the dataset the graph needs.

candlestick-series-volume.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="stockDataDc" class="io.jmix.uisamples.entity.StockData"/>
    </data>
    <layout>
        <charts:chart id="chart" height="100%" width="100%" minHeight="30em">
            <charts:title text="Data Amount: 100"/>
            <charts:tooltip trigger="AXIS">
                <charts:axisPointer type="LINE"/>
                <charts:formatterFunction>
                    <![CDATA[
                        function (params) {
                              var tar = params[0];

                       return '<b>Day:</b> ' + tar.name + '<br/><hr/>' +
                              '<b>Open: </b>' + tar.value.open + '<br/>' +
                              '<b>Close: </b>' + tar.value.close + '<br/>' +
                              '<b>High: </b>' + tar.value.high + '<br/>' +
                              '<b>Low: </b>' + tar.value.low + '<br/><hr/>' +
                              '<b>Volume: </b>' + tar.value.volume;
                            }
                    ]]>
                </charts:formatterFunction>
            </charts:tooltip>

            <charts:dataZoom>
                <charts:insideDataZoom xAxisIndexes="0, 1" start="10" end="100"/>
                <charts:sliderDataZoom show="true" xAxisIndexes="0, 1" bottom="10" start="10" end="100"/>
            </charts:dataZoom>

            <charts:grid>
                <charts:gridItem left="10%" right="10%" bottom="200"/>
                <charts:gridItem left="10%" right="10%" height="80" bottom="80"/>
            </charts:grid>

            <charts:xAxes>
                <charts:xAxis categoryBoundaryGap="false" min="dataMin" max="dataMax">
                    <charts:axisLine onZero="false"/>
                    <charts:splitLine show="false"/>
                </charts:xAxis>
                <charts:xAxis scale="false" gridIndex="1" categoryBoundaryGap="false"
                              min="dataMin" max="dataMax">
                    <charts:axisLine onZero="false"/>
                    <charts:axisTick show="false"/>
                    <charts:splitLine show="false"/>
                    <charts:axisLabel show="false"/>
                </charts:xAxis>
            </charts:xAxes>

            <charts:yAxes>
                <charts:yAxis scale="true">
                    <charts:splitArea show="true"/>
                </charts:yAxis>
                <charts:yAxis scale="true" gridIndex="1" splitNumber="2">
                    <charts:axisLabel show="false"/>
                    <charts:axisLine show="false"/>
                    <charts:axisTick show="false"/>
                    <charts:splitLine show="false"/>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="stockDataDc" categoryField="date"
                               valueFields="open, close, low, high, volume"/>
            </charts:dataSet>

            <charts:series>
                <charts:candlestick>
                    <charts:encode x="date" y="open, close, low, high"/>
                </charts:candlestick>

                <charts:bar name="Volume" xAxisIndex="1" yAxisIndex="1" large="true">
                    <charts:itemStyle color="#7fbe9e"/>
                    <charts:encode x="date" y="volume"/>
                </charts:bar>
            </charts:series>
        </charts:chart>
    </layout>
</view>




CandlestickSeriesVolumeSample.java

package io.jmix.uisamples.view.flowui.charts.series.candlestick.volume;

import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.bean.StockDataGenerator;
import io.jmix.uisamples.entity.StockData;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("candlestick-series-volume")
@ViewDescriptor("candlestick-series-volume.xml")
public class CandlestickSeriesVolumeSample extends StandardView {

    @ViewComponent
    protected CollectionContainer<StockData> stockDataDc;

    @Autowired
    protected StockDataGenerator stockDataGenerator;

    @Subscribe
    protected void onInit(InitEvent event) {
        stockDataGenerator.generateData(stockDataDc);
    }
}




StockData.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.JmixId;
import io.jmix.core.metamodel.annotation.JmixEntity;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
public class StockData {

    @JmixGeneratedValue
    @JmixId
    private UUID id;

    private LocalDate date;

    private Long value;

    private Long volume;

    private Long open;

    private Long close;

    private Long high;

    private Long low;

    public Long getLow() {
        return low;
    }

    public void setLow(Long low) {
        this.low = low;
    }

    public Long getHigh() {
        return high;
    }

    public void setHigh(Long high) {
        this.high = high;
    }

    public Long getClose() {
        return close;
    }

    public void setClose(Long close) {
        this.close = close;
    }

    public Long getOpen() {
        return open;
    }

    public void setOpen(Long open) {
        this.open = open;
    }

    public Long getVolume() {
        return volume;
    }

    public void setVolume(Long volume) {
        this.volume = volume;
    }

    public Long getValue() {
        return value;
    }

    public void setValue(Long value) {
        this.value = value;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @Override
    public String toString() {
        return "StockData{" +
                "date=" + date +
                ", value=" + value +
                ", volume=" + volume +
                ", open=" + open +
                ", close=" + close +
                ", high=" + high +
                ", low=" + low +
                '}';
    }
}




StockDataGenerator.java

package io.jmix.uisamples.bean;

import io.jmix.core.Metadata;
import io.jmix.core.TimeSource;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.uisamples.entity.StockData;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component("uisamples_StockDataGenerator")
public class StockDataGenerator {

    protected static final int DAYS_COUNT = 100;

    protected Metadata metadata;
    protected TimeSource timeSource;

    protected final Random random = new Random();

    public StockDataGenerator(TimeSource timeSource, Metadata metadata) {
        this.timeSource = timeSource;
        this.metadata = metadata;
    }

    public void generateData(CollectionContainer<StockData> stockChartDc) {
        List<StockData> items = new ArrayList<>();
        for (int i = 0; i < DAYS_COUNT; i++) {
            items.add(generateStockData(LocalDate.now().plusDays(i), i));
        }
        stockChartDc.setItems(items);
    }

    protected StockData generateStockData(LocalDate date, int i) {
        long open = Math.round(random.nextDouble() * 30 + 100);
        long close = open + Math.round(random.nextDouble() * 15 - random.nextDouble() * 10);

        long low = Math.min(open, close) - Math.round(random.nextDouble() * 5);
        long high = Math.max(open, close) + Math.round(random.nextDouble() * 5);

        long volume = Math.round(random.nextDouble() * (1000 + i)) + 100 + i;
        long value = Math.round(random.nextDouble() * 30 + 100);

        return stockData(date, value, volume, open, close, high, low);
    }

    protected StockData stockData(LocalDate date, Long value, Long volume,
                                  Long open, Long close, Long high, Long low) {
        StockData dateValueVolume = metadata.create(StockData.class);
        dateValueVolume.setDate(date);
        dateValueVolume.setValue(value);
        dateValueVolume.setVolume(volume);
        dateValueVolume.setOpen(open);
        dateValueVolume.setClose(close);
        dateValueVolume.setHigh(high);
        dateValueVolume.setLow(low);
        return dateValueVolume;
    }
}


