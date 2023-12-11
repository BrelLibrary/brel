<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" exclude-result-prefixes="#all" xmlns:utr="http://www.xbrl.org/2009/utr" xmlns:iso="http://www.xbrl.org/2003/iso4217" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:link="http://www.xbrl.org/2003/linkbase">
  <!-- The purpose of this stylesheet is to transform utr.xml (a registry) into a set of numeric element declarations annotated with valid and invalid unit declarations -->
  <!-- /bin/bash
  transform -xsl:utr2schema.xsl -s:../../../lib/utr.xml
  transform -xsl:schema2testcases.xsl -s:tmp/edgar-20101231.xsd 
  dirclean.sh .
  -->
  <xsl:output method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all"/>
  <xsl:param name="trace">true</xsl:param>
  <xsl:variable name="nsXbrli">http://www.xbrl.org/2003/instance</xsl:variable>
  <xsl:variable name="nsLink">http://www.xbrl.org/2003/linkbase</xsl:variable>
  <xsl:variable name="nsXlink">http://www.w3.org/1999/xlink</xsl:variable>
  <xsl:variable name="nsIso">http://www.xbrl.org/2003/iso4217</xsl:variable>
  <xsl:variable name="year">2010</xsl:variable>
  <xsl:variable name="edbase">edgar</xsl:variable>
  <xsl:variable name="edfile" select="concat($edbase,'-',$year,'1231')"/>
  <xsl:variable name="prefix" select="concat($edbase,'')"/>
  <xsl:variable name="nsTarget" select="concat('http://',$edbase,'/',$year,'1231')"/>
  <xsl:variable name="prefixTypes">num</xsl:variable>
  <xsl:variable name="nsTypes">http://www.xbrl.org/dtr/type/numeric</xsl:variable>
  <xsl:variable name="sp" select="' '"/>
  <xsl:variable name="nl" select="'&#xA;'"/>
  <xsl:variable name="us" select="'_'"/>
  <xsl:variable name="per" select="concat($us,'per',$us)"/>
  <xsl:variable name="skip">60</xsl:variable>
  <xsl:variable name="uriDocTypes">http://www.xbrl.org/dtr/type/numeric-2009-12-16.xsd</xsl:variable>
  <xsl:variable name="docTypes" select="doc($uriDocTypes)"/>
  <xsl:template match="/utr:utr">
    <xsl:variable name="validity" select="utr:utrIsValid(.)"/>
    <xsl:message select="$validity" terminate="no"/>
    <xsl:apply-templates select="*"/>
  </xsl:template>
  <xsl:template match="utr:units">
    <xsl:result-document href="tmp/{$edfile}.xsd" encoding="UTF-8" indent="yes" method="xml">
      <xs:schema targetNamespace="{$nsTarget}">
        <xsl:namespace name="xbrli" select="$nsXbrli"/>
        <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
        <xsl:namespace name="utr">http://www.xbrl.org/2009/utr</xsl:namespace>
        <xsl:namespace name="iso" select="$nsIso"/>
        <xsl:namespace name="{$prefix}" select="$nsTarget"/>
        <xsl:namespace name="{$prefixTypes}" select="$nsTypes"/>
        <xsl:namespace name="local">local</xsl:namespace>
        <xsl:namespace name="link">http://www.xbrl.org/2003/linkbase</xsl:namespace>
        <xsl:namespace name="xlink">http://www.w3.org/1999/xlink</xsl:namespace>
        <xsl:attribute name="elementFormDefault">qualified</xsl:attribute>
        <xs:annotation>
          <xs:documentation>The purpose of this schema is to define types and derived types for each type used in utr.xml. The documentation element in each element contains all 'good' units and some 'nogood' units.</xs:documentation>
          <xs:appinfo>
            <link:linkbaseRef xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="{$edfile}_pre.xml" xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/presentationLinkbaseRef"/>
            <link:linkbaseRef xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="{$edfile}_lab.xml" xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef"/>
            <link:linkbaseRef xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="{$edfile}_def.xml" xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/definitionLinkbaseRef"/>
            <link:roleType roleURI="http://{$edbase}/role/EntityInformation" id="EntityInformation">
              <link:definition>991 - Document - Entity Information</link:definition>
              <link:usedOn>link:presentationLink</link:usedOn>
              <link:usedOn>link:calculationLink</link:usedOn>
              <link:usedOn>link:definitionLink</link:usedOn>
            </link:roleType>
            <link:roleType roleURI="http://{$edbase}/role/DocumentInformation" id="DocumentInformation">
              <link:definition>992 - Document - Document Information</link:definition>
              <link:usedOn>link:presentationLink</link:usedOn>
              <link:usedOn>link:calculationLink</link:usedOn>
              <link:usedOn>link:definitionLink</link:usedOn>
            </link:roleType>
            <link:roleType roleURI="http://{$edbase}/role/OtherInformation" id="OtherInformation">
              <link:definition>990 - Document - Other Information</link:definition>
              <link:usedOn>link:presentationLink</link:usedOn>
              <link:usedOn>link:calculationLink</link:usedOn>
              <link:usedOn>link:definitionLink</link:usedOn>
            </link:roleType>
            <link:roleType roleURI="http://{$edbase}/role/Defaults" id="Defaults">
              <link:definition>999 - Document - Defaults</link:definition>
              <link:usedOn>link:presentationLink</link:usedOn>
              <link:usedOn>link:calculationLink</link:usedOn>
              <link:usedOn>link:definitionLink</link:usedOn>
            </link:roleType>
          </xs:appinfo>
        </xs:annotation>
        <xs:import namespace="http://www.xbrl.org/2003/instance" schemaLocation="http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd"/>
        <xs:import namespace="{$nsTypes}" schemaLocation="{$uriDocTypes}"/>
        <xs:element xbrli:periodType="duration" name="Top" substitutionGroup="xbrli:item" id="{$prefix}_Top" type="xbrli:stringItemType" abstract="true" nillable="true"/>
        <xsl:for-each-group select="utr:unit[utr:status='REC' or utr:status='CR']" group-by="utr:itemType">
          <xsl:sort data-type="text" select="@id"/>
          <xsl:comment select="$nl,current-grouping-key(),string-join(current-group()/@id,$sp),$nl"/>
          <xsl:if test="not(exists(current-group()[utr:itemType='durationItemType']))">
            <xsl:variable name="sItemType" select="current-grouping-key()"/>
            <xsl:variable name="sCapitalizedType" select="concat(upper-case(substring($sItemType,1,1)),substring($sItemType,2))"/>
            <xsl:variable name="sDerivedType" select="concat('derived',$sCapitalizedType)"/>
            <xsl:variable name="sElementName" select="concat($sCapitalizedType,'Concept')"/>
            <xsl:variable name="sDerivedElementName" select="concat('Derived',$sElementName)"/>
            <xsl:variable name="sTypePrefix">
              <xsl:choose>
                <xsl:when test="$sItemType='sharesItemType'">xbrli</xsl:when>
                <xsl:when test="$sItemType='pureItemType'">xbrli</xsl:when>
                <xsl:when test="$sItemType='monetaryItemType'">xbrli</xsl:when>
                <xsl:when test="count($docTypes//xs:complexType[@name=$sItemType])>0"><xsl:value-of select="$prefixTypes"/></xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="$prefix"/>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:variable>
            <xsl:choose>
              <xsl:when test="$sTypePrefix='xbrli'"/>
              <xsl:when test="$sTypePrefix='num'"/>
              <xsl:otherwise>
                <xs:complexType name="{$sItemType}">
                  <xs:simpleContent>
                    <xs:restriction base="xbrli:decimalItemType"/>
                  </xs:simpleContent>
                </xs:complexType>
              </xsl:otherwise>
            </xsl:choose>
            <xs:complexType name="{$sDerivedType}">
              <xs:simpleContent>
                <xs:restriction base="{$sTypePrefix}:{$sItemType}"/>
              </xs:simpleContent>
            </xs:complexType>
            <xs:element name="{$sElementName}" id="{$prefix}_{$sElementName}" type="{$sTypePrefix}:{$sItemType}" substitutionGroup="xbrli:item" nillable="true" xbrli:periodType="duration">
              <xs:annotation>
                <xsl:namespace name="" select="$nsXbrli"/>
                <xsl:element name="xs:documentation">
                  <xsl:attribute name="source">good</xsl:attribute>
                  <xsl:for-each select="current-group()[empty(utr:numeratorItemType) and empty(utr:denominatorItemType)]">
                    <xsl:call-template name="Measure">
                      <xsl:with-param name="nsUnit" select="utr:nsUnit"/>
                      <xsl:with-param name="unitId" select="utr:unitId"/>
                      <xsl:with-param name="suffix">_1</xsl:with-param>
                    </xsl:call-template>
                  </xsl:for-each>
                  <xsl:for-each select="current-group()[utr:numeratorItemType
                  or utr:denominatorItemType ]">
                    <xsl:variable name="nId" select="substring-before(utr:unitId,$us)"/>
                    <xsl:variable name="numeratorItemType" select="utr:numeratorItemType"/>
                    <xsl:variable name="nsNumeratorItemType" select="utr:nsNumeratorItemType"/>
                    <xsl:variable name="numeratorName" select="//utr:unit[utr:itemType=$numeratorItemType]/utr:unitId"/>
                    <xsl:variable name="dId" select="substring-after(utr:unitId,$per)"/>
                    <xsl:variable name="denominatorItemType" select="utr:denominatorItemType"/>
                    <xsl:variable name="nsDenominatorItemType" select="utr:nsDenominatorItemType"/>
                    <xsl:variable name="denominatorName" select="//utr:unit[utr:itemType=$denominatorItemType]/utr:unitId"/>
                    <xsl:choose>
                      <xsl:when test="empty(utr:denominatorItemType)">
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',2,$nId,$dId"/>
                        </xsl:if>
                        <xsl:for-each select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$numeratorItemType][(position() = 1 or (position() mod $skip) = 1)]">
                          <xsl:call-template name="Divide">
                            <xsl:with-param name="nsNumerator" select="utr:nsUnit"/>
                            <xsl:with-param name="sNumerator" select="utr:unitId"/>
                            <xsl:with-param name="nsDenominator" select="$nsDenominatorItemType"/>
                            <xsl:with-param name="sDenominator" select="$denominatorName"/>
                            <xsl:with-param name="suffix">_2</xsl:with-param>
                            <xsl:with-param name="id" select="concat(generate-id(),'_2',$us,$us,utr:unitId,$per,$dId)"/>
                          </xsl:call-template>
                        </xsl:for-each>
                      </xsl:when>
                      <xsl:when test="empty(utr:numeratorItemType)">
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',3,$nId,$dId"/>
                        </xsl:if>
                        <xsl:for-each select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$denominatorItemType][(position() = 1 or (position() mod $skip) = 1)]">
                          <xsl:call-template name="Divide">
                            <xsl:with-param name="nsNumerator" select="$nsNumeratorItemType"/>
                            <xsl:with-param name="sNumerator" select="$numeratorName"/>
                            <xsl:with-param name="nsDenominator" select="utr:nsUnit"/>
                            <xsl:with-param name="sDenominator" select="utr:unitId"/>
                            <xsl:with-param name="suffix">_3</xsl:with-param>
                          </xsl:call-template>
                        </xsl:for-each>
                      </xsl:when>
                      <!-- now each special case of {numerator}/{denominator} -->
                      <xsl:when test="$numeratorItemType=$denominatorItemType">
                        <!-- such as monetary/monetary with num != den -->
                        <!-- enumeration counts off every $skip'th and ratio that with its successor -->
                        <xsl:variable name="skip">50</xsl:variable>
                        <xsl:variable name="numerators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$numeratorItemType][(position() mod $skip) = 1]"/>
                        <xsl:variable name="denominators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$denominatorItemType][(position() mod $skip) = 1]"/>
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',4,$nId,$dId,count($numerators),count($denominators)"/>
                        </xsl:if>
                        <xsl:variable name="units" select="//utr:unit[utr:itemType=$numeratorItemType][(position() mod $skip) = 1]"/>
                        <xsl:for-each select="$units">
                          <xsl:variable name="i" select="position()"/>
                          <xsl:if test="(count($units) ge ($i+1))">
                            <xsl:call-template name="Divide">
                              <xsl:with-param name="nsNumerator" select="utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$units[$i+1]/utr:nsUnit"/>
                              <xsl:with-param name="sDenominator" select="$units[$i+1]/utr:unitId"/>
                              <xsl:with-param name="suffix">_4</xsl:with-param>
                            </xsl:call-template>
                          </xsl:if>
                        </xsl:for-each>
                      </xsl:when>
                      <xsl:when test="$denominatorItemType='durationItemType'">
                        <!-- is exercised by the flowItemType if that were a declared type. -->
                        <xsl:variable name="skip">5</xsl:variable>
                        <xsl:variable name="numerators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$numeratorItemType][(position() mod $skip) = 1]"/>
                        <xsl:variable name="denominators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$denominatorItemType][(position() mod $skip) = 1]"/>
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',5,$nId,$dId,count($numerators),count($denominators)"/>
                        </xsl:if>
                        <xsl:for-each select="$numerators">
                          <xsl:variable name="numeratorUnit" select="."/>
                          <xsl:for-each select="$denominators">
                            <xsl:variable name="denominatorUnit" select="."/>
                            <xsl:call-template name="Divide">
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$denominatorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sDenominator" select="$denominatorUnit/utr:unitId"/>
                              <xsl:with-param name="suffix">_5</xsl:with-param>
                            </xsl:call-template>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:when>
                      <xsl:when test="$denominatorItemType!='durationItemType'">
                        <!-- would be exercised by something like 'mileage' (length / volume) if that were a declared type. -->
                        <!-- exercised in particular by (monetary / anything) -->
                        <xsl:variable name="numerators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$numeratorItemType][(position() mod $skip) = 1]"/>
                        <xsl:variable name="denominators" select="//utr:unit[(utr:status='REC' or utr:status='CR')][utr:itemType=$denominatorItemType][(position() mod $skip) = 1]"/>
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',6,$nId,$dId,count($numerators),count($denominators)"/>
                        </xsl:if>
                        <xsl:for-each select="$numerators">
                          <xsl:variable name="numeratorUnit" select="."/>
                          <xsl:if test="empty($denominators)">
                            <xsl:call-template name="Divide">
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="'local'"/>
                              <xsl:with-param name="sDenominator" select="'u1'"/>
                              <xsl:with-param name="suffix">_6</xsl:with-param>
                            </xsl:call-template>
                            <xsl:call-template name="Divide">
                              <!-- yes, it's true, if the denominator is unconstrained then even this works -->
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$nsXbrli"/>
                              <xsl:with-param name="sDenominator" select="'shares'"/>
                              <xsl:with-param name="suffix">_6</xsl:with-param>
                            </xsl:call-template>
                            <xsl:call-template name="Divide">
                              <!-- yes, it's true, if the denominator is unconstrained then even this works -->
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$nsXbrli"/>
                              <xsl:with-param name="sDenominator" select="'pure'"/>
                              <xsl:with-param name="suffix">_6</xsl:with-param>
                            </xsl:call-template>
                            <xsl:call-template name="Divide">
                              <!-- yes, it's true, if the denominator is unconstrained then even this works -->
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$nsIso"/>
                              <xsl:with-param name="sDenominator" select="'USD'"/>
                              <xsl:with-param name="suffix">_6</xsl:with-param>
                            </xsl:call-template>
                          </xsl:if>
                          <xsl:for-each select="$denominators">
                            <xsl:variable name="denominatorUnit" select="."/>
                            <xsl:call-template name="Divide">
                              <xsl:with-param name="nsNumerator" select="$numeratorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sNumerator" select="$numeratorUnit/utr:unitId"/>
                              <xsl:with-param name="nsDenominator" select="$denominatorUnit/utr:nsUnit"/>
                              <xsl:with-param name="sDenominator" select="$denominatorUnit/utr:unitId"/>
                              <xsl:with-param name="suffix">_7</xsl:with-param>
                            </xsl:call-template>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:if test="$trace='true'">
                          <xsl:message select="'CASE',7,$nId,$dId"/>
                        </xsl:if>
                      </xsl:otherwise>
                    </xsl:choose>
                  </xsl:for-each>
                </xsl:element>
                <xsl:element name="xs:documentation">
                  <xsl:attribute name="source">nogood</xsl:attribute>
                  <xsl:choose>
                    <xsl:when test="utr:bBuiltinType($sItemType)">
                      <!-- do nothing -->
                    </xsl:when>
                    <xsl:when test="not(current-group()[utr:numeratorItemType or utr:denominatorItemType])">
                      <xsl:call-template name="Measure">
                        <xsl:with-param name="prefixUnit">local</xsl:with-param>
                        <xsl:with-param name="unitId" select="'u1'"/>
                        <xsl:with-param name="suffix">_5</xsl:with-param>
                      </xsl:call-template>
                      <xsl:for-each select="current-group()[empty(utr:numeratorItemType) and empty(utr:denominatorItemType)]">
                        <xsl:sort data-type="text" order="ascending" select="upper-case(utr:unitId)"/>
                        <xsl:if test="position()=1">
                          <xsl:call-template name="Measure">
                            <xsl:with-param name="prefixUnit">local</xsl:with-param>
                            <xsl:with-param name="unitId" select="utr:unitId"/>
                            <xsl:with-param name="suffix">_6</xsl:with-param>
                            <xsl:with-param name="id" select="concat(generate-id(),'_6',$us,$us,'x',utr:unitId)"/>
                          </xsl:call-template>
                        </xsl:if>
                      </xsl:for-each>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">local</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'u2'"/>
                        <xsl:with-param name="suffix">_7</xsl:with-param>
                      </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="matches($sItemType,'[Pp]erUnitItemType')">
                      <xsl:call-template name="Measure">
                        <xsl:with-param name="prefixUnit">local</xsl:with-param>
                        <xsl:with-param name="unitId" select="'u1'"/>
                        <xsl:with-param name="suffix">_5</xsl:with-param>
                      </xsl:call-template>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">local</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'u2'"/>
                        <xsl:with-param name="suffix">_7</xsl:with-param>
                      </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="(matches($sItemType,'[pP]erShareItemType'))">
                      <xsl:call-template name="Measure">
                        <xsl:with-param name="prefixUnit">local</xsl:with-param>
                        <xsl:with-param name="unitId" select="'u1'"/>
                        <xsl:with-param name="suffix">_51</xsl:with-param>
                      </xsl:call-template>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">xbrli</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'shares'"/>
                        <xsl:with-param name="suffix">_71</xsl:with-param>
                        <xsl:with-param name="id" select="concat(generate-id(),'_71',$us,$us,'xu1_shares')"/>
                      </xsl:call-template>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">local</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'shares'"/>
                        <xsl:with-param name="suffix">_72</xsl:with-param>
                        <xsl:with-param name="id" select="concat(generate-id(),'_72',$us,$us,'u1_xshares')"/>
                      </xsl:call-template>
                    </xsl:when>
                  </xsl:choose>
                </xsl:element>
              </xs:annotation>
            </xs:element>
            <xs:element name="{$sDerivedElementName}" id="{$prefix}_{$sDerivedElementName}" type="{$prefix}:{$sDerivedType}" substitutionGroup="xbrli:item" nillable="true" xbrli:periodType="duration">
              <xs:annotation>
                <xsl:namespace name="" select="$nsXbrli"/>
                <xsl:element name="xs:documentation">
                  <xsl:attribute name="source">nogood</xsl:attribute>
                  <xsl:choose>
                    <xsl:when test="utr:bBuiltinType($sDerivedType)"/>
                    <xsl:when test="not(current-group()[utr:numeratorItemType or utr:denominatorItemType])">
                      <xsl:call-template name="Measure">
                        <xsl:with-param name="prefixUnit">local</xsl:with-param>
                        <xsl:with-param name="unitId" select="'u1'"/>
                        <xsl:with-param name="suffix">_9</xsl:with-param>
                      </xsl:call-template>
                      <xsl:for-each select="current-group()[empty(utr:numeratorItemType) and empty(utr:denominatorItemType)]">
                        <xsl:sort data-type="text" order="ascending" select="upper-case(utr:unitId)"/>
                        <xsl:if test="position()=1">
                          <xsl:call-template name="Measure">
                            <xsl:with-param name="prefixUnit">local</xsl:with-param>
                            <xsl:with-param name="unitId" select="utr:unitId"/>
                            <xsl:with-param name="suffix">_a</xsl:with-param>
                            <xsl:with-param name="id" select="concat(generate-id(),'_a',$us,$us,'x',utr:unitId)"/>
                          </xsl:call-template>
                        </xsl:if>
                      </xsl:for-each>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">local</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'u2'"/>
                        <xsl:with-param name="suffix">_b</xsl:with-param>
                      </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="(matches($sDerivedType,'[pP]erShareItemType'))">
                      <xsl:call-template name="Measure">
                        <xsl:with-param name="prefixUnit">local</xsl:with-param>
                        <xsl:with-param name="unitId" select="'u1'"/>
                        <xsl:with-param name="suffix">_a1</xsl:with-param>
                      </xsl:call-template>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">xbrli</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'shares'"/>
                        <xsl:with-param name="suffix">_71</xsl:with-param>
                        <xsl:with-param name="id" select="concat(generate-id(),'_b1',$us,$us,'xu1_shares')"/>
                      </xsl:call-template>
                      <xsl:call-template name="Divide">
                        <xsl:with-param name="prefixNumerator">local</xsl:with-param>
                        <xsl:with-param name="sNumerator" select="'u1'"/>
                        <xsl:with-param name="prefixDenominator">local</xsl:with-param>
                        <xsl:with-param name="sDenominator" select="'shares'"/>
                        <xsl:with-param name="suffix">_72</xsl:with-param>
                        <xsl:with-param name="id" select="concat(generate-id(),'_b2',$us,$us,'u1_xshares')"/>
                      </xsl:call-template>
                    </xsl:when>
                  </xsl:choose>
                </xsl:element>
              </xs:annotation>
            </xs:element>
          </xsl:if>
        </xsl:for-each-group>
      </xs:schema>
    </xsl:result-document>
    <xsl:result-document method="xml" encoding="UTF-8" href="tmp/{$edfile}_lab.xml">

      <link:linkbase xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd" xmlns:link="http://www.xbrl.org/2003/linkbase">
        <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">

          <xsl:for-each-group select="utr:unit[utr:status='REC' or utr:status='CR']" group-by="utr:itemType">
            <xsl:sort data-type="text" select="@id"/>
            <xsl:comment select="$nl,current-grouping-key(),string-join(current-group()/@id,$sp),$nl"/>
            <xsl:if test="not(exists(current-group()[utr:itemType='durationItemType']))">              
              <xsl:variable name="sItemType" select="current-grouping-key()"/>
              <xsl:variable name="sCapitalizedType" select="concat(upper-case(substring($sItemType,1,1)),substring($sItemType,2))"/>
              <xsl:variable name="sDerivedType" select="concat('derived',$sCapitalizedType)"/>
              <xsl:variable name="sElementName" select="concat($sCapitalizedType,'Concept')"/>
              <xsl:variable name="sDerivedElementName" select="concat('Derived',$sElementName)"/>
              <xsl:variable name="sTypePrefix">
                <xsl:choose>
                  <xsl:when test="$sItemType='sharesItemType'">xbrli</xsl:when>
                  <xsl:when test="$sItemType='pureItemType'">xbrli</xsl:when>
                  <xsl:when test="$sItemType='monetaryItemType'">xbrli</xsl:when>
                  <xsl:when test="exists($docTypes/xs:schema/xs:complexType[@name=$sItemType])">num</xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="$prefixTypes"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:variable>
              <link:loc xlink:href="{$edfile}.xsd#{$prefix}_{$sElementName}" xlink:type="locator" xlink:label="{$sElementName}"/>
              <xsl:element name="link:label">
                <xsl:attribute name="xlink:type">resource</xsl:attribute>
                <xsl:attribute name="xlink:label" select="concat('label_',$sElementName)"/>
                <xsl:attribute name="xlink:role">http://www.xbrl.org/2003/role/label</xsl:attribute>
                <xsl:attribute name="xml:lang">en-US</xsl:attribute>
                <xsl:value-of select="$sElementName"/>
              </xsl:element>
              <xsl:element name="link:label">
                <xsl:attribute name="xlink:type">resource</xsl:attribute>
                <xsl:attribute name="xlink:label" select="concat('label_',$sElementName)"/>
                <xsl:attribute name="xlink:role">http://www.xbrl.org/2003/role/documentation</xsl:attribute>
                <xsl:attribute name="xml:lang">en-US</xsl:attribute>
                <xsl:value-of select="$sElementName"/>
              </xsl:element>
              <xsl:element name="link:labelArc">
                <xsl:attribute name="xlink:to" select="concat('label_',$sElementName)"/>
                <xsl:attribute name="xlink:from" select="$sElementName"/>
                <xsl:attribute name="xlink:type">arc</xsl:attribute>
                <xsl:attribute name="xlink:arcrole">http://www.xbrl.org/2003/arcrole/concept-label</xsl:attribute>
              </xsl:element>
              <link:loc xlink:href="{$edfile}.xsd#{$prefix}_{$sDerivedElementName}" xlink:type="locator" xlink:label="{$sDerivedElementName}"/>
              <xsl:element name="link:label">
                <xsl:attribute name="xlink:type">resource</xsl:attribute>
                <xsl:attribute name="xlink:label" select="concat('label_',$sDerivedElementName)"/>
                <xsl:attribute name="xlink:role">http://www.xbrl.org/2003/role/label</xsl:attribute>
                <xsl:attribute name="xml:lang">en-US</xsl:attribute>
                <xsl:value-of select="$sDerivedElementName"/>
              </xsl:element>
              <xsl:element name="link:label">
                <xsl:attribute name="xlink:type">resource</xsl:attribute>
                <xsl:attribute name="xlink:label" select="concat('label_',$sDerivedElementName)"/>
                <xsl:attribute name="xlink:role">http://www.xbrl.org/2003/role/documentation</xsl:attribute>
                <xsl:attribute name="xml:lang">en-US</xsl:attribute>
                <xsl:value-of select="$sDerivedElementName"/>
              </xsl:element>
              <xsl:element name="link:labelArc">
                <xsl:attribute name="xlink:to" select="concat('label_',$sDerivedElementName)"/>
                <xsl:attribute name="xlink:from" select="$sDerivedElementName"/>
                <xsl:attribute name="xlink:type">arc</xsl:attribute>
                <xsl:attribute name="xlink:arcrole">http://www.xbrl.org/2003/arcrole/concept-label</xsl:attribute>
              </xsl:element>
          </xsl:if>
          </xsl:for-each-group>
          <link:loc xlink:href="{$edfile}.xsd#{$prefix}_Top" xlink:type="locator" xlink:label="Top"/>
          <link:label id="label_Top" xlink:type="resource" xlink:label="label_Top" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Top</link:label>
          <link:labelArc xlink:to="label_Top" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          

          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingAddressMember" xlink:type="locator" xlink:label="AccountingAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingContactMember" xlink:type="locator" xlink:label="AccountingContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingFaxMember" xlink:type="locator" xlink:label="AccountingFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingPhoneMember" xlink:type="locator" xlink:label="AccountingPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AddressTypeDomain" xlink:type="locator" xlink:label="AddressTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentDescription" xlink:type="locator" xlink:label="AmendmentDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentFlag" xlink:type="locator" xlink:label="AmendmentFlag"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ApproximateDateOfCommencementOfProposedSaleToThePublic" xlink:type="locator" xlink:label="ApproximateDateOfCommencementOfProposedSaleToThePublic"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_BusinessContactMember" xlink:type="locator" xlink:label="BusinessContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CityAreaCode" xlink:type="locator" xlink:label="CityAreaCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactAddressMember" xlink:type="locator" xlink:label="ContactAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactFaxMember" xlink:type="locator" xlink:label="ContactFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelEmailAddress" xlink:type="locator" xlink:label="ContactPersonnelEmailAddress"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelName" xlink:type="locator" xlink:label="ContactPersonnelName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelUniformResourceLocatorURL" xlink:type="locator" xlink:label="ContactPersonnelUniformResourceLocatorURL"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonTypeDomain" xlink:type="locator" xlink:label="ContactPersonTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPhoneMember" xlink:type="locator" xlink:label="ContactPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileDescription" xlink:type="locator" xlink:label="ContainedFileInformationFileDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileName" xlink:type="locator" xlink:label="ContainedFileInformationFileName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileNumber" xlink:type="locator" xlink:label="ContainedFileInformationFileNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileType" xlink:type="locator" xlink:label="ContainedFileInformationFileType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CountryRegion" xlink:type="locator" xlink:label="CountryRegion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CurrentFiscalYearEndDate" xlink:type="locator" xlink:label="CurrentFiscalYearEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DeprecatedItemsForDEI" xlink:type="locator" xlink:label="DeprecatedItemsForDEI"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentContactMember" xlink:type="locator" xlink:label="DocumentContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCopyrightInformation" xlink:type="locator" xlink:label="DocumentCopyrightInformation"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCreationDate" xlink:type="locator" xlink:label="DocumentCreationDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDescription" xlink:type="locator" xlink:label="DocumentDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDomain" xlink:type="locator" xlink:label="DocumentDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentEffectiveDate" xlink:type="locator" xlink:label="DocumentEffectiveDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalPeriodFocus" xlink:type="locator" xlink:label="DocumentFiscalPeriodFocus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalYearFocus" xlink:type="locator" xlink:label="DocumentFiscalYearFocus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationDocumentAxis" xlink:type="locator" xlink:label="DocumentInformationDocumentAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationLineItems" xlink:type="locator" xlink:label="DocumentInformationLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationTable" xlink:type="locator" xlink:label="DocumentInformationTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationTextBlock" xlink:type="locator" xlink:label="DocumentInformationTextBlock"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentName" xlink:type="locator" xlink:label="DocumentName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodEndDate" xlink:type="locator" xlink:label="DocumentPeriodEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodStartDate" xlink:type="locator" xlink:label="DocumentPeriodStartDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSubtitle" xlink:type="locator" xlink:label="DocumentSubtitle"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSynopsis" xlink:type="locator" xlink:label="DocumentSynopsis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentTitle" xlink:type="locator" xlink:label="DocumentTitle"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentType" xlink:type="locator" xlink:label="DocumentType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityEmergingGrowthCompany" xlink:type="locator" xlink:label="EntityEmergingGrowthCompany"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentVersion" xlink:type="locator" xlink:label="DocumentVersion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitiesTable" xlink:type="locator" xlink:label="EntitiesTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAccountingStandard" xlink:type="locator" xlink:label="EntityAccountingStandard"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressDescription" xlink:type="locator" xlink:label="EntityAddressAddressDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine1" xlink:type="locator" xlink:label="EntityAddressAddressLine1"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine2" xlink:type="locator" xlink:label="EntityAddressAddressLine2"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine3" xlink:type="locator" xlink:label="EntityAddressAddressLine3"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCityOrTown" xlink:type="locator" xlink:label="EntityAddressCityOrTown"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCountry" xlink:type="locator" xlink:label="EntityAddressCountry"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesAddressTypeAxis" xlink:type="locator" xlink:label="EntityAddressesAddressTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesLineItems" xlink:type="locator" xlink:label="EntityAddressesLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesTable" xlink:type="locator" xlink:label="EntityAddressesTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressPostalZipCode" xlink:type="locator" xlink:label="EntityAddressPostalZipCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressRegion" xlink:type="locator" xlink:label="EntityAddressRegion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressStateOrProvince" xlink:type="locator" xlink:label="EntityAddressStateOrProvince"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityByLocationAxis" xlink:type="locator" xlink:label="EntityByLocationAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCentralIndexKey" xlink:type="locator" xlink:label="EntityCentralIndexKey"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCommonStockSharesOutstanding" xlink:type="locator" xlink:label="EntityCommonStockSharesOutstanding"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelContactPersonTypeAxis" xlink:type="locator" xlink:label="EntityContactPersonnelContactPersonTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelLineItems" xlink:type="locator" xlink:label="EntityContactPersonnelLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelTable" xlink:type="locator" xlink:label="EntityContactPersonnelTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCurrentReportingStatus" xlink:type="locator" xlink:label="EntityCurrentReportingStatus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDataUniversalNumberingSystemNumber" xlink:type="locator" xlink:label="EntityDataUniversalNumberingSystemNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDomain" xlink:type="locator" xlink:label="EntityDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityFilerCategory" xlink:type="locator" xlink:label="EntityFilerCategory"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityHomeCountryISOCode" xlink:type="locator" xlink:label="EntityHomeCountryISOCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationDateOfIncorporation" xlink:type="locator" xlink:label="EntityIncorporationDateOfIncorporation"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationStateCountryCode" xlink:type="locator" xlink:label="EntityIncorporationStateCountryCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:type="locator" xlink:label="EntityInformationDateToChangeFormerLegalOrRegisteredName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationFormerLegalOrRegisteredName" xlink:type="locator" xlink:label="EntityInformationFormerLegalOrRegisteredName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationLineItems" xlink:type="locator" xlink:label="EntityInformationLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLegalForm" xlink:type="locator" xlink:label="EntityLegalForm"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingDepositoryReceiptRatio" xlink:type="locator" xlink:label="EntityListingDepositoryReceiptRatio"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingDescription" xlink:type="locator" xlink:label="EntityListingDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingForeign" xlink:type="locator" xlink:label="EntityListingForeign"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingParValuePerShare" xlink:type="locator" xlink:label="EntityListingParValuePerShare"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingPrimary" xlink:type="locator" xlink:label="EntityListingPrimary"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingSecurityTradingCurrency" xlink:type="locator" xlink:label="EntityListingSecurityTradingCurrency"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingsExchangeAxis" xlink:type="locator" xlink:label="EntityListingsExchangeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingsInstrumentAxis" xlink:type="locator" xlink:label="EntityListingsInstrumentAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingsLineItems" xlink:type="locator" xlink:label="EntityListingsLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityListingsTable" xlink:type="locator" xlink:label="EntityListingsTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLocationLineItems" xlink:type="locator" xlink:label="EntityLocationLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLocationPrimary" xlink:type="locator" xlink:label="EntityLocationPrimary"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLocationTable" xlink:type="locator" xlink:label="EntityLocationTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNorthAmericanIndustryClassificationPrimary" xlink:type="locator" xlink:label="EntityNorthAmericanIndustryClassificationPrimary"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNorthAmericanIndustryClassificationsIndustryAxis" xlink:type="locator" xlink:label="EntityNorthAmericanIndustryClassificationsIndustryAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNorthAmericanIndustryClassificationsLineItems" xlink:type="locator" xlink:label="EntityNorthAmericanIndustryClassificationsLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNorthAmericanIndustryClassificationsTable" xlink:type="locator" xlink:label="EntityNorthAmericanIndustryClassificationsTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNumberOfEmployees" xlink:type="locator" xlink:label="EntityNumberOfEmployees"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationType" xlink:type="locator" xlink:label="EntityOtherIdentificationType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationValue" xlink:type="locator" xlink:label="EntityOtherIdentificationValue"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersLineItems" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersTable" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPublicFloat" xlink:type="locator" xlink:label="EntityPublicFloat"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityRegistrantName" xlink:type="locator" xlink:label="EntityRegistrantName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityReportingCurrencyISOCode" xlink:type="locator" xlink:label="EntityReportingCurrencyISOCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitySectorIndustryClassificationPrimary" xlink:type="locator" xlink:label="EntitySectorIndustryClassificationPrimary"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitySectorIndustryClassificationsLineItems" xlink:type="locator" xlink:label="EntitySectorIndustryClassificationsLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitySectorIndustryClassificationsSectorAxis" xlink:type="locator" xlink:label="EntitySectorIndustryClassificationsSectorAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitySectorIndustryClassificationsTable" xlink:type="locator" xlink:label="EntitySectorIndustryClassificationsTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityTaxIdentificationNumber" xlink:type="locator" xlink:label="EntityTaxIdentificationNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityTextBlock" xlink:type="locator" xlink:label="EntityTextBlock"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityVoluntaryFilers" xlink:type="locator" xlink:label="EntityVoluntaryFilers"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityWellKnownSeasonedIssuer" xlink:type="locator" xlink:label="EntityWellKnownSeasonedIssuer"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ExchangeDomain" xlink:type="locator" xlink:label="ExchangeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_Extension" xlink:type="locator" xlink:label="Extension"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_FormerFiscalYearEndDate" xlink:type="locator" xlink:label="FormerFiscalYearEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralFaxMember" xlink:type="locator" xlink:label="GeneralFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralPhoneMember" xlink:type="locator" xlink:label="GeneralPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_HumanResourcesContactMember" xlink:type="locator" xlink:label="HumanResourcesContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InstrumentDomain" xlink:type="locator" xlink:label="InstrumentDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsContactMember" xlink:type="locator" xlink:label="InvestorRelationsContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsFaxMember" xlink:type="locator" xlink:label="InvestorRelationsFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsPhoneMember" xlink:type="locator" xlink:label="InvestorRelationsPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalAddressMember" xlink:type="locator" xlink:label="LegalAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalContactMember" xlink:type="locator" xlink:label="LegalContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalEntityAxis" xlink:type="locator" xlink:label="LegalEntityAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalFaxMember" xlink:type="locator" xlink:label="LegalFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalPhoneMember" xlink:type="locator" xlink:label="LegalPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LocalPhoneNumber" xlink:type="locator" xlink:label="LocalPhoneNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LocationDomain" xlink:type="locator" xlink:label="LocationDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_MailingAddressMember" xlink:type="locator" xlink:label="MailingAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_NAICSDomain" xlink:type="locator" xlink:label="NAICSDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_OtherAddressMember" xlink:type="locator" xlink:label="OtherAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ParentEntityLegalName" xlink:type="locator" xlink:label="ParentEntityLegalName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberDescription" xlink:type="locator" xlink:label="PhoneFaxNumberDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberTypeDomain" xlink:type="locator" xlink:label="PhoneFaxNumberTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PostEffectiveAmendmentNumber" xlink:type="locator" xlink:label="PostEffectiveAmendmentNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PreEffectiveAmendmentNumber" xlink:type="locator" xlink:label="PreEffectiveAmendmentNumber"/>
                    <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_RegistrationStatementAmendmentNumber" xlink:type="locator" xlink:label="RegistrationStatementAmendmentNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_SectorDomain" xlink:type="locator" xlink:label="SectorDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_TradingSymbol" xlink:type="locator" xlink:label="TradingSymbol"/>

          <link:label xlink:type="resource" xlink:label="label_AccountingAddressMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Accounting Address [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_AccountingContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Accounting Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_AccountingFaxMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Accounting Fax [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_AccountingPhoneMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Accounting Phone [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_AddressTypeDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Address Type [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_AmendmentDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Amendment Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_AmendmentFlag" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Amendment Flag</link:label>
          <link:label xlink:type="resource" xlink:label="label_ApproximateDateOfCommencementOfProposedSaleToThePublic" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Approximate Date of Commencement of Proposed Sale to Public</link:label>
          <link:label xlink:type="resource" xlink:label="label_BusinessContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Business Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_CityAreaCode" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">City Area Code</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactAddressMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Address [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactFaxMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Fax [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactPersonnelEmailAddress" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Personnel Email Address</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactPersonnelName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Personnel Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactPersonnelUniformResourceLocatorURL" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Personnel Uniform Resource Locator (URL)</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactPersonTypeDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Person Type [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContactPhoneMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contact Phone [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContainedFileInformationFileDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contained File Information, File Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContainedFileInformationFileName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contained File Information, File Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContainedFileInformationFileNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contained File Information, File Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_ContainedFileInformationFileType" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Contained File Information, File Type</link:label>
          <link:label xlink:type="resource" xlink:label="label_CountryRegion" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Country Region</link:label>
          <link:label xlink:type="resource" xlink:label="label_CurrentFiscalYearEndDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Current Fiscal Year End Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_DeprecatedItemsForDEI" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Deprecated Items for DEI [Abstract]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentCopyrightInformation" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Copyright Information</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentCreationDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Creation Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentEffectiveDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Effective Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentFiscalPeriodFocus" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Fiscal Period Focus</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentFiscalYearFocus" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Fiscal Year Focus</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentInformationDocumentAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Information, Document [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentInformationLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Information [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentInformationTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Information [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentInformationTextBlock" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Information [Text Block]</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentPeriodEndDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Period End Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentPeriodStartDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Period Start Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentSubtitle" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Subtitle</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentSynopsis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Synopsis</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentTitle" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Title</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentType" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Type</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityEmergingGrowthCompany" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Emerging Grwoth Company</link:label>
          <link:label xlink:type="resource" xlink:label="label_DocumentVersion" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Document Version</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntitiesTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entities [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAccountingStandard" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Accounting Standard</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressAddressDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Address Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressAddressLine1" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Address Line One</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressAddressLine2" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Address Line Two</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressAddressLine3" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Address Line Three</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressCityOrTown" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, City or Town</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressCountry" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Country</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressesAddressTypeAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Addresses, Address Type [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressesLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Addresses [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressesTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Addresses [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressPostalZipCode" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Postal Zip Code</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressRegion" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, Region</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityAddressStateOrProvince" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Address, State or Province</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityByLocationAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity by Location [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityCentralIndexKey" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Central Index Key</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityCommonStockSharesOutstanding" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Common Stock, Shares Outstanding</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityContactPersonnelContactPersonTypeAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Contact Personnel, Contact Person Type [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityContactPersonnelLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Contact Personnel [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityContactPersonnelTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Contact Personnel [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityCurrentReportingStatus" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Current Reporting Status</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityDataUniversalNumberingSystemNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Data Universal Numbering System Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityFilerCategory" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Filer Category</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityHomeCountryISOCode" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Home Country ISO Code</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityIncorporationDateOfIncorporation" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Incorporation, Date of Incorporation</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityIncorporationStateCountryCode" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Incorporation, State Country Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Information, Date to Change Former Legal or Registered Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityInformationFormerLegalOrRegisteredName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Information, Former Legal or Registered Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityInformationLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Information [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityLegalForm" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Legal Form</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingDepositoryReceiptRatio" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Depository Receipt Ratio</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingForeign" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Foreign</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingParValuePerShare" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Par Value Per Share</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingPrimary" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Primary</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingSecurityTradingCurrency" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listing, Security Trading Currency</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingsExchangeAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listings, Exchange [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingsInstrumentAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listings, Instrument [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingsLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listings [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityListingsTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Listings [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityLocationLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Location [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityLocationPrimary" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Location, Primary</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityLocationTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Location [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityNorthAmericanIndustryClassificationPrimary" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity North American Industry Classification, Primary</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityNorthAmericanIndustryClassificationsIndustryAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity North American Industry Classifications, Industry [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityNorthAmericanIndustryClassificationsLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity North American Industry Classifications [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityNorthAmericanIndustryClassificationsTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity North American Industry Classifications [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityNumberOfEmployees" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Number of Employees</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityOtherIdentificationType" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Other Identification Type</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityOtherIdentificationValue" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Other Identification Value</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityPhoneFaxNumbersLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Phone Fax Numbers [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Phone Fax Numbers, Phone Fax Number Type [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityPhoneFaxNumbersTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Phone Fax Numbers [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityPublicFloat" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Public Float</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityRegistrantName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Registrant Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityReportingCurrencyISOCode" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Reporting Currency ISO Code</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntitySectorIndustryClassificationPrimary" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Sector Industry Classification, Primary</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntitySectorIndustryClassificationsLineItems" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Sector Industry Classifications [Line Items]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntitySectorIndustryClassificationsSectorAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Sector Industry Classifications, Sector [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntitySectorIndustryClassificationsTable" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Sector Industry Classifications [Table]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityTaxIdentificationNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Tax Identification Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityTextBlock" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity [Text Block]</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityVoluntaryFilers" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Voluntary Filers</link:label>
          <link:label xlink:type="resource" xlink:label="label_EntityWellKnownSeasonedIssuer" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Entity Well-known Seasoned Issuer</link:label>
          <link:label xlink:type="resource" xlink:label="label_ExchangeDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Exchange [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_Extension" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Extension</link:label>
          <link:label xlink:type="resource" xlink:label="label_FormerFiscalYearEndDate" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Former Fiscal Year End Date</link:label>
          <link:label xlink:type="resource" xlink:label="label_GeneralFaxMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">General Fax [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_GeneralPhoneMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">General Phone [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_HumanResourcesContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Human Resources Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_InstrumentDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Instrument [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_InvestorRelationsContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Investor Relations Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_InvestorRelationsFaxMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Investor Relations Fax [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_InvestorRelationsPhoneMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Investor Relations Phone [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LegalAddressMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Legal Address [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LegalContactMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Legal Contact [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LegalEntityAxis" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Legal Entity [Axis]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LegalFaxMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Legal Fax [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LegalPhoneMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Legal Phone [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_LocalPhoneNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Local Phone Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_LocationDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Location [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_MailingAddressMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Mailing Address [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_NAICSDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">NAICS [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_OtherAddressMember" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Other Address [Member]</link:label>
          <link:label xlink:type="resource" xlink:label="label_ParentEntityLegalName" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Parent Entity Legal Name</link:label>
          <link:label xlink:type="resource" xlink:label="label_PhoneFaxNumberDescription" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Phone Fax Number Description</link:label>
          <link:label xlink:type="resource" xlink:label="label_PhoneFaxNumberTypeDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Phone Fax Number Type [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_PostEffectiveAmendmentNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Post-Effective Amendment Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_PreEffectiveAmendmentNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Pre-Effective Amendment Number</link:label>
                    <link:label xlink:type="resource" xlink:label="label_RegistrationStatementAmendmentNumber" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Registration Statement Amendment Number</link:label>
          <link:label xlink:type="resource" xlink:label="label_SectorDomain" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Sector [Domain]</link:label>
          <link:label xlink:type="resource" xlink:label="label_TradingSymbol" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Trading Symbol</link:label>
          <link:label xlink:type="resource" xlink:label="label_DecimalItemTypeConcept" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Decimal Item Type Concept</link:label>
          <link:label xlink:type="resource" xlink:label="label_DecimalItemTypeDerivedConcept" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="en-US">Decimal Item Type Derived Concept</link:label>

          <link:labelArc xlink:to="label_AccountingAddressMember" xlink:from="AccountingAddressMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AccountingContactMember" xlink:from="AccountingContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AccountingFaxMember" xlink:from="AccountingFaxMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AccountingPhoneMember" xlink:from="AccountingPhoneMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AddressTypeDomain" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AmendmentDescription" xlink:from="AmendmentDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_AmendmentFlag" xlink:from="AmendmentFlag" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ApproximateDateOfCommencementOfProposedSaleToThePublic" xlink:from="ApproximateDateOfCommencementOfProposedSaleToThePublic" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_BusinessContactMember" xlink:from="BusinessContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_CityAreaCode" xlink:from="CityAreaCode" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactAddressMember" xlink:from="ContactAddressMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactFaxMember" xlink:from="ContactFaxMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactPersonnelEmailAddress" xlink:from="ContactPersonnelEmailAddress" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactPersonnelName" xlink:from="ContactPersonnelName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactPersonnelUniformResourceLocatorURL" xlink:from="ContactPersonnelUniformResourceLocatorURL" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactPersonTypeDomain" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContactPhoneMember" xlink:from="ContactPhoneMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContainedFileInformationFileDescription" xlink:from="ContainedFileInformationFileDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContainedFileInformationFileName" xlink:from="ContainedFileInformationFileName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContainedFileInformationFileNumber" xlink:from="ContainedFileInformationFileNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ContainedFileInformationFileType" xlink:from="ContainedFileInformationFileType" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_CountryRegion" xlink:from="CountryRegion" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_CurrentFiscalYearEndDate" xlink:from="CurrentFiscalYearEndDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DeprecatedItemsForDEI" xlink:from="DeprecatedItemsForDEI" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentContactMember" xlink:from="DocumentContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentCopyrightInformation" xlink:from="DocumentCopyrightInformation" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentCreationDate" xlink:from="DocumentCreationDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentDescription" xlink:from="DocumentDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentDomain" xlink:from="DocumentDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentEffectiveDate" xlink:from="DocumentEffectiveDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentFiscalPeriodFocus" xlink:from="DocumentFiscalPeriodFocus" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentFiscalYearFocus" xlink:from="DocumentFiscalYearFocus" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentInformationDocumentAxis" xlink:from="DocumentInformationDocumentAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentInformationLineItems" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentInformationTable" xlink:from="DocumentInformationTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentInformationTextBlock" xlink:from="DocumentInformationTextBlock" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentName" xlink:from="DocumentName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentPeriodEndDate" xlink:from="DocumentPeriodEndDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentPeriodStartDate" xlink:from="DocumentPeriodStartDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentSubtitle" xlink:from="DocumentSubtitle" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentSynopsis" xlink:from="DocumentSynopsis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentTitle" xlink:from="DocumentTitle" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentType" xlink:from="DocumentType" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityEmergingGrowthCompany" xlink:from="EntityEmergingGrowthCompany" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_DocumentVersion" xlink:from="DocumentVersion" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntitiesTable" xlink:from="EntitiesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAccountingStandard" xlink:from="EntityAccountingStandard" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressAddressDescription" xlink:from="EntityAddressAddressDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressAddressLine1" xlink:from="EntityAddressAddressLine1" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressAddressLine2" xlink:from="EntityAddressAddressLine2" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressAddressLine3" xlink:from="EntityAddressAddressLine3" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressCityOrTown" xlink:from="EntityAddressCityOrTown" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressCountry" xlink:from="EntityAddressCountry" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressesAddressTypeAxis" xlink:from="EntityAddressesAddressTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressesLineItems" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressesTable" xlink:from="EntityAddressesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressPostalZipCode" xlink:from="EntityAddressPostalZipCode" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressRegion" xlink:from="EntityAddressRegion" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityAddressStateOrProvince" xlink:from="EntityAddressStateOrProvince" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityByLocationAxis" xlink:from="EntityByLocationAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityCentralIndexKey" xlink:from="EntityCentralIndexKey" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityCommonStockSharesOutstanding" xlink:from="EntityCommonStockSharesOutstanding" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityContactPersonnelContactPersonTypeAxis" xlink:from="EntityContactPersonnelContactPersonTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityContactPersonnelLineItems" xlink:from="EntityContactPersonnelLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityContactPersonnelTable" xlink:from="EntityContactPersonnelTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityCurrentReportingStatus" xlink:from="EntityCurrentReportingStatus" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityDataUniversalNumberingSystemNumber" xlink:from="EntityDataUniversalNumberingSystemNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityDomain" xlink:from="EntityDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityFilerCategory" xlink:from="EntityFilerCategory" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityHomeCountryISOCode" xlink:from="EntityHomeCountryISOCode" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityIncorporationDateOfIncorporation" xlink:from="EntityIncorporationDateOfIncorporation" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityIncorporationStateCountryCode" xlink:from="EntityIncorporationStateCountryCode" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:from="EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityInformationFormerLegalOrRegisteredName" xlink:from="EntityInformationFormerLegalOrRegisteredName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityInformationLineItems" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityLegalForm" xlink:from="EntityLegalForm" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingDepositoryReceiptRatio" xlink:from="EntityListingDepositoryReceiptRatio" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingDescription" xlink:from="EntityListingDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingForeign" xlink:from="EntityListingForeign" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingParValuePerShare" xlink:from="EntityListingParValuePerShare" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingPrimary" xlink:from="EntityListingPrimary" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingSecurityTradingCurrency" xlink:from="EntityListingSecurityTradingCurrency" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingsExchangeAxis" xlink:from="EntityListingsExchangeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingsInstrumentAxis" xlink:from="EntityListingsInstrumentAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingsLineItems" xlink:from="EntityListingsLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityListingsTable" xlink:from="EntityListingsTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityLocationLineItems" xlink:from="EntityLocationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityLocationPrimary" xlink:from="EntityLocationPrimary" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityLocationTable" xlink:from="EntityLocationTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityNorthAmericanIndustryClassificationPrimary" xlink:from="EntityNorthAmericanIndustryClassificationPrimary" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityNorthAmericanIndustryClassificationsIndustryAxis" xlink:from="EntityNorthAmericanIndustryClassificationsIndustryAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityNorthAmericanIndustryClassificationsLineItems" xlink:from="EntityNorthAmericanIndustryClassificationsLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityNorthAmericanIndustryClassificationsTable" xlink:from="EntityNorthAmericanIndustryClassificationsTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityNumberOfEmployees" xlink:from="EntityNumberOfEmployees" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityOtherIdentificationType" xlink:from="EntityOtherIdentificationType" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityOtherIdentificationValue" xlink:from="EntityOtherIdentificationValue" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityPhoneFaxNumbersLineItems" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:from="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityPhoneFaxNumbersTable" xlink:from="EntityPhoneFaxNumbersTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityPublicFloat" xlink:from="EntityPublicFloat" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityRegistrantName" xlink:from="EntityRegistrantName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityReportingCurrencyISOCode" xlink:from="EntityReportingCurrencyISOCode" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntitySectorIndustryClassificationPrimary" xlink:from="EntitySectorIndustryClassificationPrimary" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntitySectorIndustryClassificationsLineItems" xlink:from="EntitySectorIndustryClassificationsLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntitySectorIndustryClassificationsSectorAxis" xlink:from="EntitySectorIndustryClassificationsSectorAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntitySectorIndustryClassificationsTable" xlink:from="EntitySectorIndustryClassificationsTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityTaxIdentificationNumber" xlink:from="EntityTaxIdentificationNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityTextBlock" xlink:from="EntityTextBlock" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityVoluntaryFilers" xlink:from="EntityVoluntaryFilers" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_EntityWellKnownSeasonedIssuer" xlink:from="EntityWellKnownSeasonedIssuer" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ExchangeDomain" xlink:from="ExchangeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_Extension" xlink:from="Extension" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_FormerFiscalYearEndDate" xlink:from="FormerFiscalYearEndDate" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_GeneralFaxMember" xlink:from="GeneralFaxMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_GeneralPhoneMember" xlink:from="GeneralPhoneMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_HumanResourcesContactMember" xlink:from="HumanResourcesContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_InstrumentDomain" xlink:from="InstrumentDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_InvestorRelationsContactMember" xlink:from="InvestorRelationsContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_InvestorRelationsFaxMember" xlink:from="InvestorRelationsFaxMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_InvestorRelationsPhoneMember" xlink:from="InvestorRelationsPhoneMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LegalAddressMember" xlink:from="LegalAddressMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LegalContactMember" xlink:from="LegalContactMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LegalEntityAxis" xlink:from="LegalEntityAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LegalFaxMember" xlink:from="LegalFaxMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LegalPhoneMember" xlink:from="LegalPhoneMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LocalPhoneNumber" xlink:from="LocalPhoneNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_LocationDomain" xlink:from="LocationDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_MailingAddressMember" xlink:from="MailingAddressMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_NAICSDomain" xlink:from="NAICSDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_OtherAddressMember" xlink:from="OtherAddressMember" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_ParentEntityLegalName" xlink:from="ParentEntityLegalName" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_PhoneFaxNumberDescription" xlink:from="PhoneFaxNumberDescription" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_PhoneFaxNumberTypeDomain" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_PostEffectiveAmendmentNumber" xlink:from="PostEffectiveAmendmentNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_PreEffectiveAmendmentNumber" xlink:from="PreEffectiveAmendmentNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
                    <link:labelArc xlink:to="label_RegistrationStatementAmendmentNumber" xlink:from="RegistrationStatementAmendmentNumber" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_SectorDomain" xlink:from="SectorDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
          <link:labelArc xlink:to="label_TradingSymbol" xlink:from="TradingSymbol" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
        </link:labelLink>
      </link:linkbase>

    </xsl:result-document>
    <xsl:result-document method="xml" encoding="UTF-8" href="tmp/{$edfile}_pre.xml">

      <link:linkbase xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd" xmlns:link="http://www.xbrl.org/2003/linkbase">
        <link:roleRef xlink:href="{$edfile}.xsd#DocumentInformation" roleURI="http://{$edbase}/role/DocumentInformation" xlink:type="simple"/>
        <link:roleRef xlink:href="{$edfile}.xsd#EntityInformation" roleURI="http://{$edbase}/role/EntityInformation" xlink:type="simple"/>
        <link:roleRef xlink:href="{$edfile}.xsd#OtherInformation" roleURI="http://{$edbase}/role/OtherInformation" xlink:type="simple"/>
        <link:presentationLink xlink:type="extended" xlink:role="http://{$edbase}/role/OtherInformation">
          <link:loc xlink:href="{$edfile}.xsd#{$prefix}_Top" xlink:type="locator" xlink:label="Top"/>
          
          <xsl:for-each-group select="utr:unit[utr:status='REC' or utr:status='CR']" group-by="utr:itemType">
            <xsl:sort data-type="text" select="@id"/>
            <xsl:comment select="$nl,current-grouping-key(),string-join(current-group()/@id,$sp),$nl"/>
            <xsl:variable name="order" select="position()"/>
            <xsl:if test="not(exists(current-group()[utr:itemType='durationItemType']))">              
              <xsl:variable name="sItemType" select="current-grouping-key()"/>
              <xsl:variable name="sCapitalizedType" select="concat(upper-case(substring($sItemType,1,1)),substring($sItemType,2))"/>
              <xsl:variable name="sDerivedType" select="concat('derived',$sCapitalizedType)"/>
              <xsl:variable name="sElementName" select="concat($sCapitalizedType,'Concept')"/>
              <xsl:variable name="sDerivedElementName" select="concat('Derived',$sElementName)"/>
              <xsl:variable name="sTypePrefix">
                <xsl:choose>
                  <xsl:when test="$sItemType='sharesItemType'">xbrli</xsl:when>
                  <xsl:when test="$sItemType='pureItemType'">xbrli</xsl:when>
                  <xsl:when test="$sItemType='monetaryItemType'">xbrli</xsl:when>
                  <xsl:when test="exists($docTypes/xs:schema/xs:complexType[@name=$sItemType])">num</xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="$prefixTypes"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:variable>
              <link:loc xlink:href="{$edfile}.xsd#{$prefix}_{$sElementName}" xlink:type="locator" xlink:label="{$sElementName}"/>
              <xsl:element name="link:presentationArc">
                <xsl:attribute name="xlink:to" select="concat('',$sElementName)"/>
                <xsl:attribute name="xlink:from">Top</xsl:attribute>
                <xsl:attribute name="xlink:type">arc</xsl:attribute>
                <xsl:attribute name="xlink:arcrole">http://www.xbrl.org/2003/arcrole/parent-child</xsl:attribute>
                <xsl:attribute name="order" select="10 * $order"/>
              </xsl:element>
              <link:loc xlink:href="{$edfile}.xsd#{$prefix}_{$sDerivedElementName}" xlink:type="locator" xlink:label="{$sDerivedElementName}"/>
              <xsl:element name="link:presentationArc">
                <xsl:attribute name="xlink:to" select="concat('',$sDerivedElementName)"/>
                <xsl:attribute name="xlink:from">Top</xsl:attribute>
                <xsl:attribute name="xlink:type">arc</xsl:attribute>
                <xsl:attribute name="xlink:arcrole">http://www.xbrl.org/2003/arcrole/parent-child</xsl:attribute>
                <xsl:attribute name="order" select="10 * $order + 5"/>
              </xsl:element>
            </xsl:if>
          </xsl:for-each-group>
          
                 </link:presentationLink>
        <link:presentationLink xlink:type="extended" xlink:role="http://{$edbase}/role/DocumentInformation">
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationTextBlock" xlink:type="locator" xlink:label="DocumentInformationTextBlock"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationTable" xlink:type="locator" xlink:label="DocumentInformationTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationDocumentAxis" xlink:type="locator" xlink:label="DocumentInformationDocumentAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationLineItems" xlink:type="locator" xlink:label="DocumentInformationLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDomain" xlink:type="locator" xlink:label="DocumentDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentName" xlink:type="locator" xlink:label="DocumentName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentTitle" xlink:type="locator" xlink:label="DocumentTitle"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSubtitle" xlink:type="locator" xlink:label="DocumentSubtitle"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSynopsis" xlink:type="locator" xlink:label="DocumentSynopsis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentType" xlink:type="locator" xlink:label="DocumentType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityEmergingGrowthCompany" xlink:type="locator" xlink:label="EntityEmergingGrowthCompany"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentFlag" xlink:type="locator" xlink:label="AmendmentFlag"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentDescription" xlink:type="locator" xlink:label="AmendmentDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDescription" xlink:type="locator" xlink:label="DocumentDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCreationDate" xlink:type="locator" xlink:label="DocumentCreationDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentEffectiveDate" xlink:type="locator" xlink:label="DocumentEffectiveDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodStartDate" xlink:type="locator" xlink:label="DocumentPeriodStartDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodEndDate" xlink:type="locator" xlink:label="DocumentPeriodEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalYearFocus" xlink:type="locator" xlink:label="DocumentFiscalYearFocus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalPeriodFocus" xlink:type="locator" xlink:label="DocumentFiscalPeriodFocus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentVersion" xlink:type="locator" xlink:label="DocumentVersion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCopyrightInformation" xlink:type="locator" xlink:label="DocumentCopyrightInformation"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileName" xlink:type="locator" xlink:label="ContainedFileInformationFileName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileDescription" xlink:type="locator" xlink:label="ContainedFileInformationFileDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileType" xlink:type="locator" xlink:label="ContainedFileInformationFileType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileNumber" xlink:type="locator" xlink:label="ContainedFileInformationFileNumber"/>
          <link:presentationArc xlink:to="DocumentInformationTable" use="optional" order="1.0" xlink:from="DocumentInformationTextBlock" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentInformationDocumentAxis" use="optional" order="1.0" xlink:from="DocumentInformationTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentDomain" use="optional" order="1.0" xlink:from="DocumentInformationDocumentAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentInformationLineItems" use="optional" order="2.0" xlink:from="DocumentInformationTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentName" use="optional" order="1.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentTitle" use="optional" order="2.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentSubtitle" use="optional" order="3.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentSynopsis" use="optional" order="4.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentType" use="optional" order="5.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityEmergingGrowthCompany" use="optional" order="6.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AmendmentFlag" use="optional" order="7.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AmendmentDescription" use="optional" order="8.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentDescription" use="optional" order="9.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentCreationDate" use="optional" order="10.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentEffectiveDate" use="optional" order="11.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentPeriodStartDate" use="optional" order="12.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentPeriodEndDate" use="optional" order="13.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentFiscalYearFocus" use="optional" order="14.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentFiscalPeriodFocus" use="optional" order="15.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentVersion" use="optional" order="16.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentCopyrightInformation" use="optional" order="17.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContainedFileInformationFileName" use="optional" order="18.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContainedFileInformationFileDescription" use="optional" order="19.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContainedFileInformationFileType" use="optional" order="20.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContainedFileInformationFileNumber" use="optional" order="21.0" xlink:from="DocumentInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
        </link:presentationLink>
        <link:presentationLink xlink:type="extended" xlink:role="http://{$edbase}/role/EntityInformation">
          <link:loc xlink:href="{$edfile}.xsd#{$prefix}_Top" xlink:type="locator" xlink:label="Top"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitiesTable" xlink:type="locator" xlink:label="EntitiesTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalEntityAxis" xlink:type="locator" xlink:label="LegalEntityAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationLineItems" xlink:type="locator" xlink:label="EntityInformationLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelTable" xlink:type="locator" xlink:label="EntityContactPersonnelTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelContactPersonTypeAxis" xlink:type="locator" xlink:label="EntityContactPersonnelContactPersonTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonTypeDomain" xlink:type="locator" xlink:label="ContactPersonTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelLineItems" xlink:type="locator" xlink:label="EntityContactPersonnelLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesTable" xlink:type="locator" xlink:label="EntityAddressesTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesAddressTypeAxis" xlink:type="locator" xlink:label="EntityAddressesAddressTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AddressTypeDomain" xlink:type="locator" xlink:label="AddressTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesLineItems" xlink:type="locator" xlink:label="EntityAddressesLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersTable" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersTable"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberTypeDomain" xlink:type="locator" xlink:label="PhoneFaxNumberTypeDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersLineItems" xlink:type="locator" xlink:label="EntityPhoneFaxNumbersLineItems"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityTextBlock" xlink:type="locator" xlink:label="EntityTextBlock"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDomain" xlink:type="locator" xlink:label="EntityDomain"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityRegistrantName" xlink:type="locator" xlink:label="EntityRegistrantName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCentralIndexKey" xlink:type="locator" xlink:label="EntityCentralIndexKey"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityTaxIdentificationNumber" xlink:type="locator" xlink:label="EntityTaxIdentificationNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDataUniversalNumberingSystemNumber" xlink:type="locator" xlink:label="EntityDataUniversalNumberingSystemNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationType" xlink:type="locator" xlink:label="EntityOtherIdentificationType"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationValue" xlink:type="locator" xlink:label="EntityOtherIdentificationValue"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationFormerLegalOrRegisteredName" xlink:type="locator" xlink:label="EntityInformationFormerLegalOrRegisteredName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:type="locator" xlink:label="EntityInformationDateToChangeFormerLegalOrRegisteredName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityHomeCountryISOCode" xlink:type="locator" xlink:label="EntityHomeCountryISOCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ParentEntityLegalName" xlink:type="locator" xlink:label="ParentEntityLegalName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAccountingStandard" xlink:type="locator" xlink:label="EntityAccountingStandard"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityReportingCurrencyISOCode" xlink:type="locator" xlink:label="EntityReportingCurrencyISOCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationStateCountryCode" xlink:type="locator" xlink:label="EntityIncorporationStateCountryCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationDateOfIncorporation" xlink:type="locator" xlink:label="EntityIncorporationDateOfIncorporation"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNumberOfEmployees" xlink:type="locator" xlink:label="EntityNumberOfEmployees"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CurrentFiscalYearEndDate" xlink:type="locator" xlink:label="CurrentFiscalYearEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCommonStockSharesOutstanding" xlink:type="locator" xlink:label="EntityCommonStockSharesOutstanding"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPublicFloat" xlink:type="locator" xlink:label="EntityPublicFloat"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityFilerCategory" xlink:type="locator" xlink:label="EntityFilerCategory"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCurrentReportingStatus" xlink:type="locator" xlink:label="EntityCurrentReportingStatus"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityVoluntaryFilers" xlink:type="locator" xlink:label="EntityVoluntaryFilers"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityWellKnownSeasonedIssuer" xlink:type="locator" xlink:label="EntityWellKnownSeasonedIssuer"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_FormerFiscalYearEndDate" xlink:type="locator" xlink:label="FormerFiscalYearEndDate"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLegalForm" xlink:type="locator" xlink:label="EntityLegalForm"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentContactMember" xlink:type="locator" xlink:label="DocumentContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalContactMember" xlink:type="locator" xlink:label="LegalContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingContactMember" xlink:type="locator" xlink:label="AccountingContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsContactMember" xlink:type="locator" xlink:label="InvestorRelationsContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_HumanResourcesContactMember" xlink:type="locator" xlink:label="HumanResourcesContactMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelName" xlink:type="locator" xlink:label="ContactPersonnelName"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelEmailAddress" xlink:type="locator" xlink:label="ContactPersonnelEmailAddress"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_MailingAddressMember" xlink:type="locator" xlink:label="MailingAddressMember"/>
                    <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_OtherAddressMember" xlink:type="locator" xlink:label="OtherAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalAddressMember" xlink:type="locator" xlink:label="LegalAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingAddressMember" xlink:type="locator" xlink:label="AccountingAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactAddressMember" xlink:type="locator" xlink:label="ContactAddressMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressDescription" xlink:type="locator" xlink:label="EntityAddressAddressDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine1" xlink:type="locator" xlink:label="EntityAddressAddressLine1"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine2" xlink:type="locator" xlink:label="EntityAddressAddressLine2"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine3" xlink:type="locator" xlink:label="EntityAddressAddressLine3"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCityOrTown" xlink:type="locator" xlink:label="EntityAddressCityOrTown"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressStateOrProvince" xlink:type="locator" xlink:label="EntityAddressStateOrProvince"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressRegion" xlink:type="locator" xlink:label="EntityAddressRegion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCountry" xlink:type="locator" xlink:label="EntityAddressCountry"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressPostalZipCode" xlink:type="locator" xlink:label="EntityAddressPostalZipCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsPhoneMember" xlink:type="locator" xlink:label="InvestorRelationsPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsFaxMember" xlink:type="locator" xlink:label="InvestorRelationsFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralPhoneMember" xlink:type="locator" xlink:label="GeneralPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralFaxMember" xlink:type="locator" xlink:label="GeneralFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalPhoneMember" xlink:type="locator" xlink:label="LegalPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalFaxMember" xlink:type="locator" xlink:label="LegalFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingPhoneMember" xlink:type="locator" xlink:label="AccountingPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingFaxMember" xlink:type="locator" xlink:label="AccountingFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPhoneMember" xlink:type="locator" xlink:label="ContactPhoneMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactFaxMember" xlink:type="locator" xlink:label="ContactFaxMember"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberDescription" xlink:type="locator" xlink:label="PhoneFaxNumberDescription"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CountryRegion" xlink:type="locator" xlink:label="CountryRegion"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CityAreaCode" xlink:type="locator" xlink:label="CityAreaCode"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LocalPhoneNumber" xlink:type="locator" xlink:label="LocalPhoneNumber"/>
          <link:loc xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_Extension" xlink:type="locator" xlink:label="Extension"/>
          <link:presentationArc xlink:to="EntityTextBlock" use="optional" order="1.0" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntitiesTable" use="optional" order="2.0" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalEntityAxis" use="optional" order="1.0" xlink:from="EntitiesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityDomain" use="optional" order="1.0" xlink:from="LegalEntityAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityInformationLineItems" use="optional" order="2.0" xlink:from="EntitiesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityRegistrantName" use="optional" order="1.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityCentralIndexKey" use="optional" order="2.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityTaxIdentificationNumber" use="optional" order="3.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityDataUniversalNumberingSystemNumber" use="optional" order="4.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityOtherIdentificationType" use="optional" order="5.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityOtherIdentificationValue" use="optional" order="6.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityInformationFormerLegalOrRegisteredName" use="optional" order="8.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityInformationDateToChangeFormerLegalOrRegisteredName" use="optional" order="9.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityHomeCountryISOCode" use="optional" order="11.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ParentEntityLegalName" use="optional" order="12.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAccountingStandard" use="optional" order="13.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityReportingCurrencyISOCode" use="optional" order="14.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityIncorporationStateCountryCode" use="optional" order="15.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityIncorporationDateOfIncorporation" use="optional" order="16.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityNumberOfEmployees" use="optional" order="17.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="CurrentFiscalYearEndDate" use="optional" order="18.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityCommonStockSharesOutstanding" use="optional" order="25.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityPublicFloat" use="optional" order="24.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityFilerCategory" use="optional" order="23.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityCurrentReportingStatus" use="optional" order="22.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityVoluntaryFilers" use="optional" order="21.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityWellKnownSeasonedIssuer" use="optional" order="20.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="FormerFiscalYearEndDate" use="optional" order="19.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityLegalForm" use="optional" order="10.0" xlink:from="EntityInformationLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityContactPersonnelTable" use="optional" order="3.0" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalEntityAxis" use="optional" order="1.0" xlink:from="EntityContactPersonnelTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityContactPersonnelContactPersonTypeAxis" use="optional" order="2.0" xlink:from="EntityContactPersonnelTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactPersonTypeDomain" use="optional" order="1.0" xlink:from="EntityContactPersonnelContactPersonTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="DocumentContactMember" use="optional" order="1.0" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalContactMember" use="optional" order="2.0" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AccountingContactMember" use="optional" order="4.0" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="InvestorRelationsContactMember" use="optional" order="5.0" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="HumanResourcesContactMember" use="optional" order="6.0" xlink:from="ContactPersonTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityContactPersonnelLineItems" use="optional" order="3.0" xlink:from="EntityContactPersonnelTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactPersonnelName" use="optional" order="1.0" xlink:from="EntityContactPersonnelLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactPersonnelEmailAddress" use="optional" order="2.0" xlink:from="EntityContactPersonnelLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressesTable" use="optional" order="4.0" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalEntityAxis" use="optional" order="1.0" xlink:from="EntityAddressesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressesAddressTypeAxis" use="optional" order="2.0" xlink:from="EntityAddressesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AddressTypeDomain" use="optional" order="1.0" xlink:from="EntityAddressesAddressTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="MailingAddressMember" use="optional" order="1.0" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
                    <link:presentationArc xlink:to="OtherAddressMember" use="optional" order="3.0" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalAddressMember" use="optional" order="4.0" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AccountingAddressMember" use="optional" order="5.0" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactAddressMember" use="optional" order="6.0" xlink:from="AddressTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressesLineItems" use="optional" order="3.0" xlink:from="EntityAddressesTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressAddressDescription" use="optional" order="1.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressAddressLine1" use="optional" order="2.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressAddressLine2" use="optional" order="3.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressAddressLine3" use="optional" order="4.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressCityOrTown" use="optional" order="5.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressStateOrProvince" use="optional" order="6.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressRegion" use="optional" order="7.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressCountry" use="optional" order="8.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityAddressPostalZipCode" use="optional" order="9.0" xlink:from="EntityAddressesLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityPhoneFaxNumbersTable" use="optional" order="5.0" xlink:from="Top" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalEntityAxis" use="optional" order="1.0" xlink:from="EntityPhoneFaxNumbersTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" use="optional" order="2.0" xlink:from="EntityPhoneFaxNumbersTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="PhoneFaxNumberTypeDomain" use="optional" order="1.0" xlink:from="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="InvestorRelationsPhoneMember" use="optional" order="1.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="InvestorRelationsFaxMember" use="optional" order="2.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="GeneralPhoneMember" use="optional" order="3.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="GeneralFaxMember" use="optional" order="4.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalPhoneMember" use="optional" order="5.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LegalFaxMember" use="optional" order="6.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AccountingPhoneMember" use="optional" order="7.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="AccountingFaxMember" use="optional" order="8.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactPhoneMember" use="optional" order="9.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="ContactFaxMember" use="optional" order="10.0" xlink:from="PhoneFaxNumberTypeDomain" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="EntityPhoneFaxNumbersLineItems" use="optional" order="3.0" xlink:from="EntityPhoneFaxNumbersTable" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="PhoneFaxNumberDescription" use="optional" order="1.0" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="CountryRegion" use="optional" order="2.0" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="CityAreaCode" use="optional" order="3.0" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="LocalPhoneNumber" use="optional" order="4.0" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
          <link:presentationArc xlink:to="Extension" use="optional" order="5.0" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child"/>
        </link:presentationLink>
      </link:linkbase>
    </xsl:result-document>
    <xsl:result-document method="xml" encoding="UTF-8" href="tmp/{$edfile}_def.xml">
      
      <link:linkbase xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xbrldt="http://xbrl.org/2005/xbrldt">
        <link:roleRef roleURI="http://edgar/role/DocumentInformation" xlink:type="simple" xlink:href="edgar-20101231.xsd#DocumentInformation"/>
        <link:roleRef roleURI="http://edgar/role/EntityInformation" xlink:type="simple" xlink:href="edgar-20101231.xsd#EntityInformation"/>
        <link:roleRef roleURI="http://edgar/role/Defaults" xlink:type="simple" xlink:href="edgar-20101231.xsd#Defaults"/>
        <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/all" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#all"/>
        <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#dimension-default"/>
        <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#dimension-domain"/>
        <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/domain-member" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#domain-member"/>
        <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#hypercube-dimension"/>
        <link:definitionLink xlink:type="extended" xlink:role="http://edgar/role/DocumentInformation">
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationLineItems" xlink:label="DocumentInformationLineItems"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationTable" xlink:label="DocumentInformationTable"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationDocumentAxis" xlink:label="DocumentInformationDocumentAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDomain" xlink:label="DocumentDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentName" xlink:label="DocumentName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentTitle" xlink:label="DocumentTitle"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSubtitle" xlink:label="DocumentSubtitle"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentSynopsis" xlink:label="DocumentSynopsis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentType" xlink:label="DocumentType"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityEmergingGrowthCompany" xlink:label="EntityEmergingGrowthCompany"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentFlag" xlink:label="AmendmentFlag"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AmendmentDescription" xlink:label="AmendmentDescription"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDescription" xlink:label="DocumentDescription"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCreationDate" xlink:label="DocumentCreationDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentEffectiveDate" xlink:label="DocumentEffectiveDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodStartDate" xlink:label="DocumentPeriodStartDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentPeriodEndDate" xlink:label="DocumentPeriodEndDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalYearFocus" xlink:label="DocumentFiscalYearFocus"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentFiscalPeriodFocus" xlink:label="DocumentFiscalPeriodFocus"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentVersion" xlink:label="DocumentVersion"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentCopyrightInformation" xlink:label="DocumentCopyrightInformation"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileName" xlink:label="ContainedFileInformationFileName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileDescription" xlink:label="ContainedFileInformationFileDescription"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileType" xlink:label="ContainedFileInformationFileType"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContainedFileInformationFileNumber" xlink:label="ContainedFileInformationFileNumber"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="DocumentInformationLineItems" xlink:to="DocumentInformationTable" use="optional" order="1.0" xbrldt:contextElement="segment"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="DocumentInformationTable" xlink:to="DocumentInformationDocumentAxis" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:from="DocumentInformationDocumentAxis" xlink:to="DocumentDomain" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentName" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentTitle" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentSubtitle" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentSynopsis" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentType" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="EntityEmergingGrowthCompany" use="optional" order="7.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="AmendmentFlag" use="optional" order="8.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="AmendmentDescription" use="optional" order="9.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentDescription" use="optional" order="10.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentCreationDate" use="optional" order="11.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentEffectiveDate" use="optional" order="12.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentPeriodStartDate" use="optional" order="13.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentPeriodEndDate" use="optional" order="14.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentFiscalYearFocus" use="optional" order="15.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentFiscalPeriodFocus" use="optional" order="16.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentVersion" use="optional" order="17.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="DocumentCopyrightInformation" use="optional" order="18.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="ContainedFileInformationFileName" use="optional" order="19.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="ContainedFileInformationFileDescription" use="optional" order="20.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="ContainedFileInformationFileType" use="optional" order="21.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="DocumentInformationLineItems" xlink:to="ContainedFileInformationFileNumber" use="optional" order="22.0"/>
        </link:definitionLink>
        <link:definitionLink  xlink:type="extended" xlink:role="http://{$edbase}/role/EntityInformation">
          <link:loc xlink:href="{$edfile}.xsd#{$prefix}_Top" xlink:type="locator" xlink:label="Top"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationLineItems" xlink:label="EntityInformationLineItems"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntitiesTable" xlink:label="EntitiesTable"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalEntityAxis" xlink:label="LegalEntityAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelLineItems" xlink:label="EntityContactPersonnelLineItems"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelTable" xlink:label="EntityContactPersonnelTable"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelContactPersonTypeAxis" xlink:label="EntityContactPersonnelContactPersonTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonTypeDomain" xlink:label="ContactPersonTypeDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesLineItems" xlink:label="EntityAddressesLineItems"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesTable" xlink:label="EntityAddressesTable"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesAddressTypeAxis" xlink:label="EntityAddressesAddressTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AddressTypeDomain" xlink:label="AddressTypeDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersLineItems" xlink:label="EntityPhoneFaxNumbersLineItems"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersTable" xlink:label="EntityPhoneFaxNumbersTable"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:label="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberTypeDomain" xlink:label="PhoneFaxNumberTypeDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDomain" xlink:label="EntityDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityRegistrantName" xlink:label="EntityRegistrantName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCentralIndexKey" xlink:label="EntityCentralIndexKey"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityTaxIdentificationNumber" xlink:label="EntityTaxIdentificationNumber"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDataUniversalNumberingSystemNumber" xlink:label="EntityDataUniversalNumberingSystemNumber"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationType" xlink:label="EntityOtherIdentificationType"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityOtherIdentificationValue" xlink:label="EntityOtherIdentificationValue"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationFormerLegalOrRegisteredName" xlink:label="EntityInformationFormerLegalOrRegisteredName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityInformationDateToChangeFormerLegalOrRegisteredName" xlink:label="EntityInformationDateToChangeFormerLegalOrRegisteredName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityLegalForm" xlink:label="EntityLegalForm"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityHomeCountryISOCode" xlink:label="EntityHomeCountryISOCode"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ParentEntityLegalName" xlink:label="ParentEntityLegalName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAccountingStandard" xlink:label="EntityAccountingStandard"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityReportingCurrencyISOCode" xlink:label="EntityReportingCurrencyISOCode"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationStateCountryCode" xlink:label="EntityIncorporationStateCountryCode"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityIncorporationDateOfIncorporation" xlink:label="EntityIncorporationDateOfIncorporation"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityNumberOfEmployees" xlink:label="EntityNumberOfEmployees"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CurrentFiscalYearEndDate" xlink:label="CurrentFiscalYearEndDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_FormerFiscalYearEndDate" xlink:label="FormerFiscalYearEndDate"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityWellKnownSeasonedIssuer" xlink:label="EntityWellKnownSeasonedIssuer"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityVoluntaryFilers" xlink:label="EntityVoluntaryFilers"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCurrentReportingStatus" xlink:label="EntityCurrentReportingStatus"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityFilerCategory" xlink:label="EntityFilerCategory"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPublicFloat" xlink:label="EntityPublicFloat"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityCommonStockSharesOutstanding" xlink:label="EntityCommonStockSharesOutstanding"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonTypeDomain" xlink:label="ContactPersonTypeDomain_2"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentContactMember" xlink:label="DocumentContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalContactMember" xlink:label="LegalContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_BusinessContactMember" xlink:label="BusinessContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingContactMember" xlink:label="AccountingContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsContactMember" xlink:label="InvestorRelationsContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_HumanResourcesContactMember" xlink:label="HumanResourcesContactMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelName" xlink:label="ContactPersonnelName"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelEmailAddress" xlink:label="ContactPersonnelEmailAddress"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonnelUniformResourceLocatorURL" xlink:label="ContactPersonnelUniformResourceLocatorURL"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AddressTypeDomain" xlink:label="AddressTypeDomain_2"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_MailingAddressMember" xlink:label="MailingAddressMember"/>
                    <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_OtherAddressMember" xlink:label="OtherAddressMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalAddressMember" xlink:label="LegalAddressMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingAddressMember" xlink:label="AccountingAddressMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactAddressMember" xlink:label="ContactAddressMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressDescription" xlink:label="EntityAddressAddressDescription"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine1" xlink:label="EntityAddressAddressLine1"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine2" xlink:label="EntityAddressAddressLine2"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressAddressLine3" xlink:label="EntityAddressAddressLine3"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCityOrTown" xlink:label="EntityAddressCityOrTown"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressStateOrProvince" xlink:label="EntityAddressStateOrProvince"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressRegion" xlink:label="EntityAddressRegion"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressCountry" xlink:label="EntityAddressCountry"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressPostalZipCode" xlink:label="EntityAddressPostalZipCode"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberTypeDomain" xlink:label="PhoneFaxNumberTypeDomain_2"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsPhoneMember" xlink:label="InvestorRelationsPhoneMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_InvestorRelationsFaxMember" xlink:label="InvestorRelationsFaxMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralPhoneMember" xlink:label="GeneralPhoneMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_GeneralFaxMember" xlink:label="GeneralFaxMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalPhoneMember" xlink:label="LegalPhoneMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalFaxMember" xlink:label="LegalFaxMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingPhoneMember" xlink:label="AccountingPhoneMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AccountingFaxMember" xlink:label="AccountingFaxMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPhoneMember" xlink:label="ContactPhoneMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactFaxMember" xlink:label="ContactFaxMember"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberDescription" xlink:label="PhoneFaxNumberDescription"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CountryRegion" xlink:label="CountryRegion"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_CityAreaCode" xlink:label="CityAreaCode"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LocalPhoneNumber" xlink:label="LocalPhoneNumber"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_Extension" xlink:label="Extension"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="Top" xlink:to="EntityInformationLineItems" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="EntityInformationLineItems" xlink:to="EntitiesTable" use="optional" order="1.0" xbrldt:contextElement="segment"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntitiesTable" xlink:to="LegalEntityAxis" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:from="LegalEntityAxis" xlink:to="EntityDomain" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityRegistrantName" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityCentralIndexKey" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityTaxIdentificationNumber" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityDataUniversalNumberingSystemNumber" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityOtherIdentificationType" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityOtherIdentificationValue" use="optional" order="7.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityInformationFormerLegalOrRegisteredName" use="optional" order="8.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityInformationDateToChangeFormerLegalOrRegisteredName" use="optional" order="9.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityLegalForm" use="optional" order="10.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityHomeCountryISOCode" use="optional" order="11.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="ParentEntityLegalName" use="optional" order="12.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityAccountingStandard" use="optional" order="13.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityReportingCurrencyISOCode" use="optional" order="14.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityIncorporationStateCountryCode" use="optional" order="15.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityIncorporationDateOfIncorporation" use="optional" order="16.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityNumberOfEmployees" use="optional" order="17.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="CurrentFiscalYearEndDate" use="optional" order="18.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="FormerFiscalYearEndDate" use="optional" order="19.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityWellKnownSeasonedIssuer" use="optional" order="20.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityVoluntaryFilers" use="optional" order="21.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityCurrentReportingStatus" use="optional" order="22.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityFilerCategory" use="optional" order="23.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityPublicFloat" use="optional" order="24.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityInformationLineItems" xlink:to="EntityCommonStockSharesOutstanding" use="optional" order="25.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="Top" xlink:to="EntityContactPersonnelLineItems" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="EntityContactPersonnelLineItems" xlink:to="EntityContactPersonnelTable" use="optional" order="1.0" xbrldt:contextElement="segment"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityContactPersonnelTable" xlink:to="LegalEntityAxis" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityContactPersonnelTable" xlink:to="EntityContactPersonnelContactPersonTypeAxis" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:from="EntityContactPersonnelContactPersonTypeAxis" xlink:to="ContactPersonTypeDomain_2" use="optional" priority="1" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="DocumentContactMember" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="LegalContactMember" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="BusinessContactMember" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="AccountingContactMember" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="InvestorRelationsContactMember" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="ContactPersonTypeDomain" xlink:to="HumanResourcesContactMember" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityContactPersonnelLineItems" xlink:to="ContactPersonnelName" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityContactPersonnelLineItems" xlink:to="ContactPersonnelEmailAddress" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityContactPersonnelLineItems" xlink:to="ContactPersonnelUniformResourceLocatorURL" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="Top" xlink:to="EntityAddressesLineItems" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressesTable" use="optional" order="1.0" xbrldt:contextElement="segment"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityAddressesTable" xlink:to="LegalEntityAxis" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityAddressesTable" xlink:to="EntityAddressesAddressTypeAxis" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:from="EntityAddressesAddressTypeAxis" xlink:to="AddressTypeDomain_2" use="optional" priority="1" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="AddressTypeDomain" xlink:to="MailingAddressMember" use="optional" order="1.0"/>
                    <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="AddressTypeDomain" xlink:to="OtherAddressMember" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="AddressTypeDomain" xlink:to="LegalAddressMember" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="AddressTypeDomain" xlink:to="AccountingAddressMember" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="AddressTypeDomain" xlink:to="ContactAddressMember" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressAddressDescription" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressAddressLine1" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressAddressLine2" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressAddressLine3" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressCityOrTown" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressStateOrProvince" use="optional" order="7.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressRegion" use="optional" order="8.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressCountry" use="optional" order="9.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityAddressesLineItems" xlink:to="EntityAddressPostalZipCode" use="optional" order="10.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="Top" xlink:to="EntityPhoneFaxNumbersLineItems" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="EntityPhoneFaxNumbersTable" use="optional" order="1.0" xbrldt:contextElement="segment"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityPhoneFaxNumbersTable" xlink:to="LegalEntityAxis" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="EntityPhoneFaxNumbersTable" xlink:to="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:from="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:to="PhoneFaxNumberTypeDomain_2" use="optional" priority="1" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="InvestorRelationsPhoneMember" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="InvestorRelationsFaxMember" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="GeneralPhoneMember" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="GeneralFaxMember" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="LegalPhoneMember" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="LegalFaxMember" use="optional" order="6.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="AccountingPhoneMember" use="optional" order="7.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="AccountingFaxMember" use="optional" order="8.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="ContactPhoneMember" use="optional" order="9.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="PhoneFaxNumberTypeDomain" xlink:to="ContactFaxMember" use="optional" order="10.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="PhoneFaxNumberDescription" use="optional" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="CountryRegion" use="optional" order="3.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="CityAreaCode" use="optional" order="4.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="LocalPhoneNumber" use="optional" order="5.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="EntityPhoneFaxNumbersLineItems" xlink:to="Extension" use="optional" order="6.0"/>
        </link:definitionLink>
        <link:definitionLink xlink:type="extended" xlink:role="http://edgar/role/Defaults">
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentInformationDocumentAxis" xlink:label="DocumentInformationDocumentAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_LegalEntityAxis" xlink:label="LegalEntityAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityContactPersonnelContactPersonTypeAxis" xlink:label="EntityContactPersonnelContactPersonTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityAddressesAddressTypeAxis" xlink:label="EntityAddressesAddressTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:label="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_DocumentDomain" xlink:label="DocumentDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_EntityDomain" xlink:label="EntityDomain_2"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_ContactPersonTypeDomain" xlink:label="ContactPersonTypeDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_AddressTypeDomain" xlink:label="AddressTypeDomain"/>
          <link:loc xlink:type="locator" xlink:href="https://xbrl.sec.gov/dei/2018/dei-2018-01-31.xsd#dei_PhoneFaxNumberTypeDomain" xlink:label="PhoneFaxNumberTypeDomain"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:from="DocumentInformationDocumentAxis" xlink:to="DocumentDomain" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:from="LegalEntityAxis" xlink:to="EntityDomain_2" use="optional" priority="1" order="2.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:from="EntityContactPersonnelContactPersonTypeAxis" xlink:to="ContactPersonTypeDomain" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:from="EntityAddressesAddressTypeAxis" xlink:to="AddressTypeDomain" use="optional" order="1.0"/>
          <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/dimension-default" xlink:from="EntityPhoneFaxNumbersPhoneFaxNumberTypeAxis" xlink:to="PhoneFaxNumberTypeDomain" use="optional" order="1.0"/>
        </link:definitionLink>
      </link:linkbase>
    </xsl:result-document>
  </xsl:template>

  <xsl:template name="Measure">
    <xsl:param name="nsUnit"/>
    <xsl:param name="prefixUnit" select="utr:nsPrefix($nsUnit)"/>
    <xsl:param name="unitId"/>
    <xsl:param name="suffix"/>
    <xsl:param name="id" select="concat(generate-id(),$suffix,$us,$us,$unitId)"/>

    <xsl:element name="unit" namespace="{$nsXbrli}">
      <xsl:attribute name="id" select="$id"/>
      <xsl:element name="measure" namespace="{$nsXbrli}">
        <xsl:value-of select="concat($prefixUnit,':',$unitId)"/>
      </xsl:element>
    </xsl:element>
  </xsl:template>
  <xsl:template name="Divide">
    <xsl:param name="nsNumerator"/>
    <xsl:param name="prefixNumerator" select="utr:nsPrefix($nsNumerator)"/>
    <xsl:param name="sNumerator"/>

    <xsl:param name="nsDenominator"/>
    <xsl:param name="prefixDenominator" select="utr:nsPrefix($nsDenominator)"/>
    <xsl:param name="sDenominator"/>
    <xsl:param name="suffix"/>
    <xsl:param name="id" select="concat(generate-id(),$suffix,$us,$us,$sNumerator,$us,$sDenominator)"/>

    <xsl:element name="unit" namespace="{$nsXbrli}">
      <xsl:attribute name="id" select="$id"/>
      <xsl:element name="divide" namespace="{$nsXbrli}">
        <xsl:element name="unitNumerator" namespace="{$nsXbrli}">
          <xsl:element name="measure" namespace="{$nsXbrli}">
            <xsl:value-of select="concat($prefixNumerator,':',$sNumerator)"/>
          </xsl:element>
        </xsl:element>
        <xsl:element name="unitDenominator" namespace="{$nsXbrli}">
          <xsl:element name="measure" namespace="{$nsXbrli}">
            <xsl:value-of select="concat($prefixDenominator,':',$sDenominator)"/>
          </xsl:element>
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:function name="utr:bBuiltinType" as="xs:boolean">
    <xsl:param name="type"/>
    <xsl:value-of select="matches($type,'(([mM]onetaryItemType)|([sS]haresItemType))')"/>
  </xsl:function>

  <xsl:function name="utr:nsPrefix">
    <xsl:param name="ns"/>
    <xsl:choose>
      <xsl:when test="($ns eq $nsXbrli)">xbrli</xsl:when>
      <xsl:when test="($ns eq $nsIso)">iso</xsl:when>
      <xsl:when test="($ns eq 'local')">local</xsl:when>
      <xsl:when test="($ns eq $nsTarget)">
        <xsl:value-of select="$prefix"/>
      </xsl:when>
      <xsl:otherwise>utr</xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <xsl:function name="utr:utrIsValid">
    <xsl:param name="root"/>
    <xsl:for-each-group select="$root/descendant-or-self::utr:unit" group-by="concat(utr:status,$sp,'{',utr:nsUnit,'}',utr:unitId)">
      <xsl:choose>
        <xsl:when test="count(current-group())=1"/>
        <xsl:otherwise>
          <xsl:message terminate="yes" select="concat('MORE THAN ONE MATCH OF ''',current-grouping-key(),''' AT ',string-join(current-group()/@id,','))"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:function>

</xsl:stylesheet>
