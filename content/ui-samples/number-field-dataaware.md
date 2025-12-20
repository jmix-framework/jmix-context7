<Path>Components > NumberField > Data-aware NumberField</Path>

The dataContainer and property attributes are used to connect the NumberField to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

number-field-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="pointDc"
                  class="io.jmix.uisamples.entity.Point"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <numberField id="numberField" label="Field connected to a container" width="15em"
                         dataContainer="pointDc" property="x"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




NumberFieldDataawareSample.java

package io.jmix.uisamples.view.flowui.components.numberfield.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.textfield.NumberField;
import io.jmix.core.Metadata;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Point;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("number-field-dataaware")
@ViewDescriptor("number-field-dataaware.xml")
public class NumberFieldDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Point> pointDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        Point point = metadata.create(Point.class);
        point.setX(31.32);
        pointDc.setItem(point);
    }

    @Subscribe("numberField")
    protected void onNumberFieldValueChange(ComponentValueChangeEvent<NumberField, Number> changeEvent) {
        spanValue.setText(String.valueOf(pointDc.getItem().getX()));
    }
}




Point.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@JmixEntity
@Table(name = "POINT")
@Entity
public class Point {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "X")
    private Double x;

    @Column(name = "Y")
    private Double y;

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}

