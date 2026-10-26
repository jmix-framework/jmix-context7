<Path>Add-ons > Charts > Series > Funnel series > Simple Funnel series</Path>

Basically a FunnelSeries is a graphical representation that resembles the shape of a funnel where each segment gets progressively narrower. The segments are arranged vertically to showcase a hierarchy.

funnel-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data>
        <collection id="titleValueDc"
                    class="io.jmix.uisamples.entity.TitleValue">
            <fetchPlan extends="_local"/>
            <loader id="titleValueDl">
                <query>
                    <![CDATA[select e from TitleValue e order by e.value desc]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:dataSet>
                <charts:source dataContainer="titleValueDc" categoryField="title" valueFields="value"/>
            </charts:dataSet>

            <charts:series>
                <charts:funnel name="Client activity"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




FunnelSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.funnel.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("funnel-series-simple")
@ViewDescriptor("funnel-series-simple.xml")
public class FunnelSeriesSimpleSample extends StandardView {
}




TitleValue.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "TITLE_VALUE")
@Entity
public class TitleValue {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @NotNull
    @Column(name = "TITLE", nullable = false)
    private String title;

    @NotNull
    @Column(name = "VALUE_", nullable = false)
    private Integer value;

    public Integer getValue() {
        return value;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"title", "value"})
    public String getInstanceName() {
        return String.format("%s - %s", title, value);
    }
}


