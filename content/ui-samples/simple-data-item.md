<Path>Add-ons > Charts > Data items > SimpleDataItem</Path>

ListChartItems can be used to populate chart component data without using dataContainer. SimpleDataItem takes an instance of any public class from which the data for the chart will be taken.

simple-data-item.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="SimpleDataItem" right="10%"/>
            <charts:legend/>

            <charts:series>
                <charts:pie startAngle="45"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




SimpleDataItemSample.java

package io.jmix.uisamples.view.flowui.charts.dataitems.simpledataitem;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.SimpleDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

@ViewController("simple-data-item")
@ViewDescriptor("simple-data-item.xml")
public class SimpleDataItemSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<SimpleDataItem> chartItems = new ListChartItems<>(
                new SimpleDataItem(new ValueDescription(75, "Sky")),
                new SimpleDataItem(new ValueDescription(7, "Shady side of pyramid")),
                new SimpleDataItem(new ValueDescription(18, "Sunny side of pyramid"))
        );

        chart.withDataSet(
                new DataSet().withSource(
                        new DataSet.Source<SimpleDataItem>()
                                .withDataProvider(chartItems)
                                .withCategoryField("description")
                                .withValueField("value")
                )
        );
    }

    public static class ValueDescription {
        protected Integer value;
        protected String description;

        public ValueDescription(Integer value, String description) {
            this.value = value;
            this.description = description;
        }

        public Integer getValue() {
            return value;
        }

        public String getDescription() {
            return description;
        }
    }
}


