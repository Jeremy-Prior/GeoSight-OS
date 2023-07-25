/**
* GeoSight is UNICEF's geospatial web-based business intelligence platform.
*
* Contact : geosight-no-reply@unicef.org
*
* .. note:: This program is free software; you can redistribute it and/or modify
*     it under the terms of the GNU Affero General Public License as published by
*     the Free Software Foundation; either version 3 of the License, or
*     (at your option) any later version.
*
* __author__ = 'irwan@kartoza.com'
* __date__ = '13/06/2023'
* __copyright__ = ('Copyright 2023, Unicef')
*/

/**
 * WIDGETS reducer
 */


export const FILTERS_ACTION_NAME = 'FILTERS';
export const FILTERS_ACTION_TYPE_UPDATE = 'FILTERS/UPDATE';

const initialState = []
export default function filtersReducer(state = initialState, action) {
  if (action.name === FILTERS_ACTION_NAME) {
    switch (action.type) {
      case FILTERS_ACTION_TYPE_UPDATE: {
        return { ...action.payload }
      }
      default:
        return state
    }
  }
}