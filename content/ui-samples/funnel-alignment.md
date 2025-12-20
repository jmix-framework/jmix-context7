<Path>Add-ons > Charts > Series > Funnel series > Funnel series alignment</Path>

This sample shows what alignments of a FunnelSeries.

funnel-alignment.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" height="100%" width="100%" minHeight="30em">
            <charts:title text="Funnel Comapre" left="left" top="bottom"/>
            <charts:tooltip trigger="ITEM" formatter="{a} &lt;br/&gt;{b} : {c}%"/>
            <charts:legend orientation="VERTICAL" left="left"/>

            <charts:series>
                <charts:funnel name="Pyramid"
                               width="40%" left="5%" top="5%"
                               sort="ASCENDING" funnelAlign="RIGHT"/>
                <charts:funnel name="Pyramid"
                               width="40%" left="55%" top="5%"
                               funnelAlign="LEFT"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




FunnelAlignmentSample.java

package io.jmix.uisamples.view.flowui.charts.series.funnel.alignment;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("funnel-alignment")
@ViewDescriptor("funnel-alignment.xml")
public class FunnelAlignmentSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                new MapDataItem(Map.of("name", "Product A", "value", 100)),
                new MapDataItem(Map.of("name", "Product B", "value", 80)),
                new MapDataItem(Map.of("name", "Product C", "value", 60)),
                new MapDataItem(Map.of("name", "Product D", "value", 30)),
                new MapDataItem(Map.of("name", "Product E", "value", 10))
        );

        chart.setDataSet(
                new DataSet().withSource(
                        new DataSet.Source<MapDataItem>()
                                .withDataProvider(items)
                                .withCategoryField("name")
                                .withValueFields("value")
                )
        );
    }
}


