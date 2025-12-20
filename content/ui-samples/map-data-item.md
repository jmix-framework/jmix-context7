<Path>Add-ons > Charts > Data items > MapDataItem</Path>

ListChartItems can be used to populate chart component data without using dataContainer. MapDataItem is a set of key:value pairs from which the data for the chart will be taken.

map-data-item.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="MapDataItem" right="10%"/>
            <charts:legend/>

            <charts:series>
                <charts:pie startAngle="45"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




MapDataItemSample.java

package io.jmix.uisamples.view.flowui.charts.dataitems.mapdataitem;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("map-data-item")
@ViewDescriptor("map-data-item.xml")
public class MapDataItemSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<MapDataItem> chartItems = new ListChartItems<>(
                new MapDataItem(Map.of("value", 75, "description", "Sky")),
                new MapDataItem(Map.of("value", 7, "description", "Shady side of pyramid")),
                new MapDataItem(Map.of("value", 18, "description", "Sunny side of pyramid"))
        );

        chart.withDataSet(
                new DataSet().withSource(
                        new DataSet.Source<MapDataItem>()
                                .withDataProvider(chartItems)
                                .withCategoryField("description")
                                .withValueField("value")
                )
        );
    }
}


