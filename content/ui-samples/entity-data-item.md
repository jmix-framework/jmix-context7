<Path>Add-ons > Charts > Data items > EntityDataItem</Path>

ListChartItems can be used to populate chart component data without using dataContainer. EntityDataItem takes an instance of any entity from which the data for the chart will be taken.

entity-data-item.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="EntityDataItem" right="10%"/>
            <charts:legend/>

            <charts:series>
                <charts:pie startAngle="45"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




EntityDataItemSample.java

package io.jmix.uisamples.view.flowui.charts.dataitems.entitydataitem;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.EntityDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.core.Metadata;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.ValueDescription;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("entity-data-item")
@ViewDescriptor("entity-data-item.xml")
public class EntityDataItemSample extends StandardView {

    @Autowired
    protected Metadata metadata;

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<EntityDataItem> chartItems = new ListChartItems<>(
                new EntityDataItem(createValueDescriptionEntity(75, "Sky")),
                new EntityDataItem(createValueDescriptionEntity(7, "Shady side of pyramid")),
                new EntityDataItem(createValueDescriptionEntity(18, "Sunny side of pyramid"))
        );

        chart.withDataSet(
                new DataSet().withSource(
                        new DataSet.Source<EntityDataItem>()
                                .withDataProvider(chartItems)
                                .withCategoryField("description")
                                .withValueField("value")
                )
        );
    }

    protected ValueDescription createValueDescriptionEntity(Integer value, String description) {
        ValueDescription entity = metadata.create(ValueDescription.class);
        entity.setValue(value);
        entity.setDescription(description);
        return entity;
    }
}




ValueDescription.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.JmixId;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.core.metamodel.annotation.JmixProperty;

import java.util.UUID;

@JmixEntity
public class ValueDescription {

    @JmixGeneratedValue
    @JmixId
    private UUID id;

    @JmixProperty(mandatory = true)
    private Integer value;

    @JmixProperty(mandatory = true)
    private String description;

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getValue() {
        return value;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


