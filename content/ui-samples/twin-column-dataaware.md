<Path>Components > TwinColumn > Data-aware TwinColumn</Path>

The dataContainer and property attributes are used to connect the twinColumn to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

twin-column-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <instance id="productDc"
                  class="io.jmix.uisamples.entity.Product"
                  fetchPlan="_local">
        </instance>
        <collection id="productTagsDc"
                    class="io.jmix.uisamples.entity.ProductTag"
                    fetchPlan="_local">
            <loader id="productTagsDl" readOnly="true">
                <query>
                    <![CDATA[select e from ProductTag e order by e.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <twinColumn id="twinColumn" label="Tags" itemsColumnLabel="Available tags"
                    selectedItemsColumnLabel="Selected tags" itemsContainer="productTagsDc"
                    dataContainer="productDc" property="tags"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




TwinColumnDataawareSample.java

package io.jmix.uisamples.view.flowui.components.twincolumn.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import io.jmix.core.Metadata;
import io.jmix.flowui.component.twincolumn.TwinColumn;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Product;
import io.jmix.uisamples.entity.ProductTag;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.stream.Collectors;

@ViewController("twin-column-dataaware")
@ViewDescriptor("twin-column-dataaware.xml")
public class TwinColumnDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Product> productDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        Product product = metadata.create(Product.class);
        productDc.setItem(product);
    }

    @Subscribe("twinColumn")
    protected void onTwinColumnValueChange(ComponentValueChangeEvent<TwinColumn<Product>, Product> event) {
        if (productDc.getItem().getTags() == null) {
            return;
        }

        spanValue.setText(getSelectedTagsInstanceName());
    }

    protected String getSelectedTagsInstanceName() {
        return productDc.getItem().getTags()
                .stream()
                .map(ProductTag::getInstanceName)
                .collect(Collectors.joining(", "));
    }
}




Product.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Table(name = "PRODUCT")
@Entity
@JmixEntity
public class Product {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", nullable = false)
    @InstanceName
    protected String name;

    @Column(name = "PRICE", nullable = false)
    protected BigDecimal price;

    @JoinTable(name = "PRODUCT_PRODUCT_TAG_LINK",
            joinColumns = @JoinColumn(name = "PRODUCT_ID"),
            inverseJoinColumns = @JoinColumn(name = "PRODUCT_TAG_ID"))
    @ManyToMany
    private List<ProductTag> tags;

    public Product() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public List<ProductTag> getTags() {
        return tags;
    }

    public void setTags(List<ProductTag> tags) {
        this.tags = tags;
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

