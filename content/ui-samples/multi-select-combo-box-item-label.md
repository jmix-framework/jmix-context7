<Path>Components > MultiSelectComboBox > MultiSelectComboBox with item label generator</Path>

This example shows how you can set up custom items label generation.

multi-select-combo-box-item-label.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="productTagsDc"
                    class="io.jmix.uisamples.entity.ProductTag"
                    fetchPlan="_local">
            <loader id="productTagsDl">
                <query>
                    <![CDATA[select e from ProductTag e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <multiSelectComboBox id="multiSelectComboBox" label="Product tags" itemsContainer="productTagsDc"/>
    </layout>
</view>




MultiSelectComboBoxItemLabelSample.java

package io.jmix.uisamples.view.flowui.components.multiselectcombobox.itemlabel;

import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.ProductTag;

@ViewController("multi-select-combo-box-item-label")
@ViewDescriptor("multi-select-combo-box-item-label.xml")
public class MultiSelectComboBoxItemLabelSample extends StandardView {

    @Install(to = "multiSelectComboBox", subject = "itemLabelGenerator")
    protected String multiSelectComboBoxItemLabelGenerator(ProductTag productTag) {
        return "#" + productTag.getName();
    }
}




ProductTag.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@JmixEntity
@Table(name = "PRODUCT_TAG")
@Entity
public class ProductTag {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "NAME")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"name"})
    public String getInstanceName() {
        return String.format("%s", name);
    }
}

